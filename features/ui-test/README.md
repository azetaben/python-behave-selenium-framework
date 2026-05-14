# UI Test Tag Commands

Quick CI-targeted `behave` commands for `inventory_item_page.feature`.

## Tag model

- `@ui-test` and `@inventory_item` are set at feature level.
- `@smoke` marks fast core checks.
- `@regression` marks full coverage scenarios.

## Commands

### Smoke subset (fast)

```powershell
python -m behave --tags "@ui-test and @inventory_item and @smoke"
```

### Regression subset (all inventory item scenarios)

```powershell
python -m behave --tags "@ui-test and @inventory_item and @regression"
```

### Regression-only (exclude smoke)

```powershell
python -m behave --tags "@ui-test and @inventory_item and @regression and not @smoke"
```

### Optional: scope to just this feature file

```powershell
python -m behave --tags "@ui-test and @inventory_item and @smoke" features/ui-test/inventory_item_page.feature
python -m behave --tags "@ui-test and @inventory_item and @regression" features/ui-test/inventory_item_page.feature
python -m behave --tags "@ui-test and @inventory_item and @regression and not @smoke" features/ui-test/inventory_item_page.feature
```

