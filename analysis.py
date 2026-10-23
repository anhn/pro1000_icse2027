"""Reproduces the RQ2 analyses (Tables VI-VII and text) from team_level_dataset.csv.
Requires: pandas, numpy, scipy, statsmodels."""
import pandas as pd, numpy as np, scipy.stats as st, statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
d = pd.read_csv('team_level_dataset.csv')
for c in ['completed_activities','on_time','late','max_scores','logins','resubmissions']:
    d[c+'_pm'] = d[c] / d.members_on_platform
d['resubmission_rate'] = d.resubmissions / d.first_submissions
cols = ['final_grade_0_10','completed_activities_pm','on_time_pm','late_pm','mean_platform_score','max_scores_pm','logins_pm','resubmissions_pm','resubmission_rate']
print('Spearman rho (p):')
for i,a in enumerate(cols):
    print(a, ['%.2f (%.3f)' % st.spearmanr(d[a], d[b]) for b in cols[:i]])
def ci(r, n): z, se = np.arctanh(r), 1.06/np.sqrt(n-3); return np.tanh([z-1.96*se, z+1.96*se]).round(2)
for v in ['completed_activities_pm','resubmissions_pm','resubmission_rate','mean_platform_score','logins_pm']:
    r, p = st.spearmanr(d.final_grade_0_10, d[v]); print(v, round(r,2), 'CI', ci(r, len(d)))
R = d[['final_grade_0_10','resubmission_rate','completed_activities_pm','mean_platform_score']].rank()
res = lambda y: sm.OLS(R[y], sm.add_constant(R[['completed_activities_pm','mean_platform_score']])).fit().resid
print('Partial rank corr (rate vs grade | completion, score):', st.pearsonr(res('final_grade_0_10'), res('resubmission_rate')))
for outcome in ['nonoverlap_criteria_mean_0_5','grade_unadjusted_0_10']:
    print(outcome, {v: tuple(np.round(st.spearmanr(d[outcome], d[v]), 3)) for v in ['completed_activities_pm','resubmission_rate','mean_platform_score','resubmissions_pm','logins_pm']})
print('Team-task completions vs grade:', st.spearmanr(d.final_grade_0_10, d.team_task_completions), ci(st.spearmanr(d.final_grade_0_10, d.team_task_completions)[0], len(d)))
hi = d.completed_activities_pm > d.completed_activities_pm.median()
print('Median split U:', st.mannwhitneyu(d[hi].final_grade_0_10, d[~hi].final_grade_0_10))
specs = [['mean_platform_score','completed_activities_pm'], ['mean_platform_score','resubmissions_pm'],
         ['mean_platform_score','completed_activities_pm','resubmissions_pm'], ['mean_platform_score','completed_activities_pm','resubmission_rate']]
for name, sub in [('all', d), ('without GB03', d[d.team!='GB03']), ('without GN01', d[d.team!='GN01'])]:
    for c in specs:
        X = sm.add_constant(sub[c]); m = sm.OLS(sub.final_grade_0_10, X).fit()
        print(f'\n[{name}] {c}\n', m.summary().tables[1], f'\nR2={m.rsquared:.3f} adjR2={m.rsquared_adj:.3f}',
              'maxVIF=%.2f' % max(vif(X.values,i) for i in range(1,X.shape[1])), "maxCook=%.2f" % m.get_influence().cooks_distance[0].max())
