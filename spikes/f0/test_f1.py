"""F1 domain/reference and serialized workbook contracts. Not Excel evaluation."""
from dataclasses import replace
from datetime import date, timedelta
from io import BytesIO
import json
import math
from pathlib import Path
import unittest
from unittest.mock import patch
from zipfile import ZipFile
from xml.etree import ElementTree as ET

from fastapi.testclient import TestClient
from openpyxl import load_workbook
from openpyxl.worksheet._writer import ALL_TEMP_FILES
from app import app, MAX_BYTES, XLSX_TYPE
from model import Activity, Wbs, Schedule, normalize, parse_xml
from engine.domain import Settings, InputError, weight_bases, reporting_weeks, distribute, prepare
from engine.distribution.auto import decide_distribution, load_rules
from engine.service import convert
from engine.workbook import render, FIRST, total_formula, cumulative_formula, last_value_formula
from test_runtime import fixture


def schedule():
    # Nested WBS, cross-year/month and an explicit milestone with nonzero duration.
    w = (Wbs('w1', '1', 'A', 'Structure', None), Wbs('w2', '2', 'A.1', 'Floor', 'w1'))
    a = Activity('a1', '1', 'EARLY', 'Early task', 'w2', date(2026,1,23), date(2026,1,30),
                 8.5, 'Duration', 'PT8H30M', '', False)
    b = replace(a, key='a2', source_object_id='2', source_id='LATE', name='Late task',
                start=date(2026,2,1), finish=date(2026,2,13), duration_hours=25.5)
    m = replace(a, key='a3', source_id='MS', name='Milestone', milestone=True,
                start=date(2026,2,13), finish=date(2026,2,13), duration_hours=99)
    return Schedule('context', 'hash', 'MSP', 'project', w, (a,b,m), (('Name','Reference'),))


def workbook(settings=Settings('Duration')):
    s = schedule()
    return load_workbook(BytesIO(render(s, settings, prepare(s, settings))))


def activity_rows(ws):
    return [r for r in range(5, ws.max_row+1)
            if ws.cell(r,1).value == 'Activity' and ws.cell(r,4).value == 'P']


class DomainTests(unittest.TestCase):
    def test_explicit_settings_and_defaults(self):
        self.assertEqual(Settings('Equal').cutoff, 'Friday')
        self.assertEqual(Settings('Equal').distribution, 'auto')
        for args in [('',), ('Amount',), ('Equal','Funday'), ('Equal','Friday','random')]:
            with self.assertRaises(InputError): Settings(*args)

    def test_weights_milestones_full_denominator(self):
        self.assertEqual(weight_bases(schedule(),'Equal'), [1,1,0])
        self.assertEqual(weight_bases(schedule(),'Duration'), [8.5,25.5,0])
        # Independent acceptance oracle; workbook formulas tested separately.
        weights = weight_bases(schedule(),'Duration')
        self.assertAlmostEqual(sum(w*p for w,p in zip(weights,[.2,.4,1]))/sum(weights), .35)
        self.assertAlmostEqual(weights[0]*.2/sum(weights), .05)

    def test_invalid_duration_and_all_milestones(self):
        s = schedule()
        for d in (None, 0, -1, float('nan'), float('inf')):
            bad = replace(s, activities=(replace(s.activities[0], duration_hours=d),))
            with self.assertRaisesRegex(InputError, 'EARLY'): weight_bases(bad, 'Duration')
        with self.assertRaises(InputError): weight_bases(replace(s,activities=(s.activities[2],)), 'Equal')
        ordinary_zero = replace(s.activities[0], duration_hours=0, finish=s.activities[0].start)
        self.assertEqual(weight_bases(replace(s, activities=(ordinary_zero,)), 'Equal'), [1])

    def test_msp_duration_minutes_without_display_format(self):
        raw = fixture('msp', True).replace(b'<DurationFormat>7</DurationFormat>', b'')
        s = normalize(parse_xml(raw),raw,production=True)
        self.assertTrue(all(a.duration_hours == 8.5 for a in s.activities))
        weight_bases(s, 'Duration')
        raw = raw.replace(b'PT8H30M0S',b'P1D')
        with self.assertRaises(InputError):
            weight_bases(normalize(parse_xml(raw),raw,production=True),'Duration')

    def test_all_weekdays_year_leap_boundaries(self):
        from engine.domain import WEEKDAYS
        for start, finish in [(date(2025,12,30),date(2026,1,9)),(date(2028,2,28),date(2028,3,3))]:
            a = replace(schedule().activities[0],start=start,finish=finish)
            s = replace(schedule(),activities=(a,))
            for day in WEEKDAYS:
                weeks = reporting_weeks(s,day)
                self.assertTrue(all(x.weekday()==WEEKDAYS.index(day) for x in weeks))
                self.assertTrue(weeks[0]-timedelta(days=6)<=start<=weeks[0])
                self.assertTrue(weeks[-1]-timedelta(days=6)<=finish<=weeks[-1])
                self.assertTrue(all((b-a).days==7 for a,b in zip(weeks,weeks[1:])))

    def test_all_distributions_close_and_partial_week_adjustment(self):
        a = replace(schedule().activities[0], start=date(2026,1,29),finish=date(2026,2,13))
        weeks = [date(2026,1,30),date(2026,2,6),date(2026,2,13)]
        for method in ('flat','front','back','bell'):
            profile = distribute(a,weeks,method)
            self.assertAlmostEqual(sum(profile),1)
            self.assertTrue(all(v>=0 for v in profile))
        self.assertAlmostEqual(distribute(a,weeks,'flat')[0],2/16)
        self.assertEqual(distribute(replace(a,start=a.finish),weeks,'bell'),[None,None,1])

    def test_auto_priority_and_fallback(self):
        rules=load_rules()
        def choose(code,wbs,name):
            return decide_distribution(activity_code=code,wbs=wbs,activity_name=name,rules=rules).distribution
        self.assertEqual(choose(' COMM-01 ','earthwork','installation'),'back')
        self.assertEqual(choose('A','foundation','testing'),'front')
        self.assertEqual(choose('A','z','installation'),'bell')
        self.assertEqual(choose('A','z','unknown'),'flat')

    def test_missing_dates_warning_and_no_usable_dates(self):
        s=schedule(); a=replace(s.activities[0],start=None)
        p=prepare(replace(s,activities=(a,s.activities[1])),Settings('Equal'))
        self.assertTrue(all(v is None for v in p[2][0])); self.assertEqual(len(p[-1]),1)
        with self.assertRaises(InputError): prepare(replace(s,activities=(a,)),Settings('Equal'))


class WorkbookTests(unittest.TestCase):
    def setUp(self): self.w=workbook()
    def tearDown(self): self.w.close()

    def test_weekly_increment_and_total_contract(self):
        ws=self.w['Main']; rows=activity_rows(ws)
        for r in rows:
            self.assertEqual(ws.cell(r+1,11).value, total_formula(f'N{r+1}:Q{r+1}'))
            self.assertTrue(all(ws.cell(r+1,c).value is None for c in range(14,18)))
            self.assertTrue(all(not ws.cell(r+1,c).protection.locked for c in range(14,18)))
        self.assertEqual(ws.cell(rows[2],9).value,0)
        validation=ws.data_validations.dataValidation[0]
        self.assertEqual((validation.type,validation.operator,validation.formula1,validation.formula2),('decimal','between','0','1'))
        self.assertTrue(validation.allow_blank)
        self.assertTrue(ws.conditional_formatting)

    def test_rollup_excludes_summary_and_does_not_renormalize_missing(self):
        ws=self.w['Main']
        for r in [5,6,7,8,9,10]:
            formula=ws.cell(r,14).value
            self.assertIn('COUNTIFS',formula); self.assertIn('SUMPRODUCT',formula)
            self.assertIn('"Activity"',formula); self.assertIn(f'/$I{r}',formula)
            self.assertNotIn('Activity Amount',formula)
            self.assertIn('SUMIFS',ws.cell(r,9).value)

    def test_cumulative_and_monthly_last_nonblank(self):
        ws=self.w['Main']
        sc=next(r for r in range(1,ws.max_row+1) if ws.cell(r,3).value=='Period Plan')
        self.assertEqual(ws.cell(sc+3,15).value,cumulative_formula(f'N{sc+2}',f'O{sc+2}',f'Q{sc+2}'))
        self.assertEqual(self.w['Monthly'].cell(sc+3,14).value,last_value_formula(f"'Main'!N{sc+3}:O{sc+3}"))
        self.assertIn('COUNT',self.w['Monthly'].cell(sc+2,15).value)

    def test_monthly_cutoff_buckets_and_percent_complete_fix(self):
        ws=self.w['Monthly']; main=self.w['Main']
        self.assertEqual(ws['N4'].value.date(),date(2026,1,30))
        self.assertEqual(ws['O4'].value.date(),date(2026,2,13))
        for r in activity_rows(main):
            for rr in (r,r+1): self.assertEqual(ws.cell(rr,11).value,total_formula(f'N{rr}:O{rr}'))
            self.assertEqual(ws.cell(r+1,14).value,total_formula(f"'Main'!N{r+1}:O{r+1}"))
            self.assertEqual(ws.cell(r+1,15).value,total_formula(f"'Main'!P{r+1}:Q{r+1}"))
            self.assertEqual(ws.row_dimensions[r].outlineLevel,main.row_dimensions[r].outlineLevel)
            self.assertTrue(ws.cell(r+1,14).protection.locked)
        early,late,_=activity_rows(main)
        self.assertAlmostEqual(ws.cell(early,14).value,1)
        self.assertAlmostEqual(ws.cell(late,15).value,1)

    def test_dashboard_df1_lookup_mask_and_zero_presence(self):
        data=self.w['Dashboard_Data']; progress=self.w['progress']
        self.assertIn('LOOKUP',data['L2'].value)
        self.assertIn('$C$2:$C$5<>""',data['L2'].value)
        self.assertNotIn('K5',data['L2'].value)
        self.assertIn('G2>Dashboard!$K$5',data['I2'].value)
        self.assertIn('NA()',data['I2'].value)
        self.assertIn('COUNTIFS',data['O2'].value)  # missing != recorded zero marker
        self.assertNotIn('Dashboard!',progress['C2'].value)
        self.assertEqual(self.w['Dashboard']['G5'].value,'Monthly')
        for address in ('B10','F10'):
            self.assertIn('<=K5',self.w['Dashboard'][address].value)
        self.assertIn('Main!$G$2',data.cell(2,32).value)
        self.assertIn('Monthly!$G$2',data.cell(2,40).value)

    def test_amount_identity_input_roundtrip_and_independence(self):
        ws=self.w['Activity Amount']; rows=[r for r in range(4,ws.max_row+1) if ws.cell(r,7).value]
        self.assertEqual(len(rows),3)
        for r in rows:
            self.assertTrue(ws.cell(r,1).value.startswith('=Main!'))
            self.assertFalse(ws.cell(r,4).protection.locked)
            self.assertIn('"Missing"',ws.cell(r,7).value)
        ws.cell(rows[1],4,0);ws.cell(rows[2],4,1500)
        out=BytesIO();self.w.save(out)
        w=load_workbook(BytesIO(out.getvalue()))
        self.assertIsNone(w['Activity Amount'].cell(rows[0],4).value)
        self.assertEqual(w['Activity Amount'].cell(rows[1],4).value,0)
        self.assertEqual(w['Activity Amount'].cell(rows[2],4).value,1500)
        for row in w['Main']:
            for cell in row:
                if cell.data_type=='f': self.assertNotIn('Activity Amount',cell.value)
        w.close()

    def test_package_charts_protection_calculation_and_safe_text(self):
        self.assertEqual(self.w.calculation.calcMode,'manual')
        self.assertTrue(self.w.calculation.calcOnSave and self.w.calculation.fullCalcOnLoad)
        for name in ('Main','Monthly','Activity Amount','Dashboard'):
            self.assertTrue(self.w[name].protection.sheet)
        self.assertEqual(self.w['_Metadata'].sheet_state,'veryHidden')
        for name in ('Main','Monthly','Dashboard'):
            self.assertEqual(len(self.w[name]._charts),1)
            self.assertEqual(len(self.w[name]._charts[0].series),5)
        s=schedule();s=replace(s,activities=(replace(s.activities[0],name='=HYPERLINK("bad")'),))
        blob=render(s,Settings('Equal'),prepare(s,Settings('Equal')))
        with ZipFile(BytesIO(blob)) as z:
            self.assertIsNone(z.testzip())
            self.assertFalse(any('externalLink' in n for n in z.namelist()))
            for n in z.namelist():
                if n.endswith('.xml'): ET.fromstring(z.read(n))
        w=load_workbook(BytesIO(blob));r=activity_rows(w['Main'])[0]
        self.assertEqual(w['Main'].cell(r,3).data_type,'s');w.close()


class F1RuntimeTests(unittest.TestCase):
    def setUp(self): self.client=TestClient(app)
    def post(self, raw, query='method=Equal'):
        return self.client.post('/api/progress/convert?'+query,content=raw,headers={'Content-Type':'application/xml'})

    def test_sources_methods_defaults_headers_integrity(self):
        for source in ('msp','p6'):
            for method in ('Equal','Duration'):
                before=set(ALL_TEMP_FILES)
                response=self.post(fixture(source,True),'method='+method)
                self.assertEqual(response.status_code,200,response.text[:100] if response.status_code!=200 else '')
                self.assertEqual(response.headers['content-type'],XLSX_TYPE)
                self.assertIn('progress.xlsx',response.headers['content-disposition'])
                w=load_workbook(BytesIO(response.content))
                metadata=dict((r[0].value,r[1].value) for r in w['_Metadata'] if r[0].value!='activity')
                self.assertEqual(metadata['weekly_cutoff'],'Friday');self.assertEqual(metadata['plan_distribution'],'auto')
                self.assertIn('Dashboard',w.sheetnames);w.close()
                self.assertEqual(set(ALL_TEMP_FILES),before)

    def test_overrides(self):
        response=self.post(fixture('msp',True),'method=Duration&cutoff=Wednesday&distribution=back')
        self.assertEqual(response.status_code,200)
        w=load_workbook(BytesIO(response.content))
        self.assertEqual(w['Main']['N4'].value.weekday(),2)
        self.assertIn('back',[row[1].value for row in w['_Metadata']]);w.close()

    def test_invalid_requests_and_safe_errors(self):
        for raw,query,status in [(b'','method=Equal',400),(b'<bad','method=Equal',400),
            (b'<unknown/>','method=Equal',422),(fixture('msp'),'method=Duration',422),
            (fixture('msp'),'method=Amount',422),(fixture('msp'),'',422),
            (fixture('msp'),'method=Equal&cutoff=wrong',422),
            (fixture('msp'),'method=Equal&distribution=wrong',422),
            (fixture('msp'),'method=Equal&cutoff=Friday&cutoff=Sunday',422),
            (b'<!DOCTYPE x [<!ENTITY y "bad">]><x>&y;</x>','method=Equal',422),
            (b'x'*(MAX_BYTES+1),'method=Equal',413)]:
            with self.subTest(query=query,status=status):
                r=self.post(raw,query);self.assertEqual(r.status_code,status)
                self.assertEqual(r.headers['cache-control'],'no-store')
        with patch('app.convert_f1',side_effect=RuntimeError('PRIVATE DATA')):
            r=self.post(fixture('msp'));self.assertEqual(r.status_code,500)
            self.assertNotIn('PRIVATE',r.text)

    def test_missing_date_warning_and_late_output(self):
        raw=fixture('msp',True)
        root=parse_xml(raw);root.find('Tasks/Task[Summary="0"]/Start').text=''
        response=self.post(ET.tostring(root))
        self.assertEqual(response.status_code,200);self.assertEqual(response.headers['X-Bluebird-Warnings'],'1')
        with patch('app.convert_f1',return_value=(b'x'*(MAX_BYTES+1),{})):
            self.assertEqual(self.post(raw).status_code,413)
        with patch('app.convert_f1',return_value=(b'PK',{})),patch('app.monotonic',side_effect=[0,61]):
            self.assertEqual(self.post(raw).status_code,504)


if __name__=='__main__': unittest.main()
