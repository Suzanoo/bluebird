# Reused Progress Studio source

Reference repository: https://github.com/Suzanoo/progress-studio/tree/89a6b80c06b986c4ec412b2717dc3e248a3537ec

- distribution/auto.py, curves.py, distribution_rules.json: copied from
  progress_studio/services/distribution/, without arithmetic changes.
- export_theme.py: copied from progress_studio/infrastructure/excel/.
- dashboard_theme.json: copied from progress_studio/config/.
- domain.distribute: coordinate-free adaptation of distribution_workbook.distribute.
- workbook.py: adapts progress_workbook, monthly_main_workbook (accepted MS-2 total
  fix), and Live Dashboard DF-1 display formulas to Bluebird's workbook layout.

No runtime dependency on the Progress Studio repository. Source identities and
XML normalization reuse the Bluebird F0 adapter with explicit F1 policy options.
No F0 proof formula is silently promoted to the production progress contract.
