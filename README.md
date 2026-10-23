# Supplementary material (anonymised)

- `team_level_dataset.csv`: platform measures and final project grade (0-10, size-adjusted) for the 22 teams in RQ2. Team codes are course codes (GB = campus, GN = online, Gol = study centre). Includes the final grade, the grade before the team-composition adjustment, and the mean of the five rubric criteria without a matching platform assignment. Counts are team totals after removing 19 duplicate submission records (identical student, task, attempt number, and timestamp); divide by `members_on_platform` for per-member measures.
- `analysis.py` / `analysis_output.txt`: reproduces the Spearman correlations, median split, and OLS models (with standard errors and the sensitivity analyses) reported in the paper.
- `score_change_by_task.csv`: score change between consecutive submissions per task (87 pairs).
- `revision_assessment.csv`: comparison of 25 exported before/after submission pairs against the concerns in the earlier feedback (uptake class, agreement with score change).
- `codebook.md`: coding framework, inclusion rules, decision rules, and negative cases for RQ1.
- `survey_instrument.md`: survey items (English translation).
- `survey_aggregate.csv`: response distributions for each item (40 respondents).

Reflection reports and raw platform logs contain personal data and are not shared (GDPR).
