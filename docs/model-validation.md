# Model validation checklist

Before operational use:
- Define claim-level labels with domain experts and document their provenance.
- Split by time/provider to reduce leakage; retain a locked holdout set.
- Report precision, recall, PR-AUC, calibration, subgroup performance, and confidence intervals.
- Choose thresholds based on review capacity and error costs.
- Monitor drift and periodically revalidate.
- Keep humans in control; log explanations and overrides.
- Complete privacy, security, legal, and compliance review.

The bundled Isolation Forest is trained on synthetic random data and is not a meaningful claims fraud detector.
