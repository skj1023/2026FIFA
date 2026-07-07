# 2026FIFA repo agent rules

## Knockout-stage prediction rule

For all future knockout matches (`g:"KO"`, including R16, quarterfinals, semifinals, third-place match, and final), predictions must never use a draw as the final outcome.

Required format for new `pred` objects on knockout matches:
- `ph` / `pa` must represent a decisive predicted score whenever possible.
- `winner` must be `"h"` or `"a"`; do not set `winner:"d"` for knockout predictions.
- If analysis expects 90 minutes to be level, still include the final winner in the prediction copy, e.g. “90分钟可能胶着/打平，但最终晋级：法国（加时/点球）”.
- Prediction UI should make the final advancing team clear with “最终晋级：<team>”.
- Group-stage predictions may still use draws when appropriate.

When updating match results, do not mark a match done before match start + 120 minutes unless ESPN/FIFA/BBC explicitly shows FT/FT-Pens. Cross-verify ESPN first, then FIFA/BBC where available.
