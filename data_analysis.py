import pandas as pd
import sqlite3
from scipy import stats
import numpy as np
import plotly.express as px

def create_summary(db_name='loblow_bio.sqlite'):
    conn = sqlite3.connect(db_name)
    
    # get count of samples
    query = '''
        SELECT 
            t.sample_id AS sample,
            t.b_cell,
            t.cd8_t_cell,
            t.cd4_t_cell,
            t.nk_cell,
            t.monocyte
        FROM treatments t
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    df['total_count'] = df[populations].sum(axis=1)
    
    # create dataframe row for each sample/population
    melted_df = df.melt(
        id_vars=['sample', 'total_count'],
        value_vars=populations,
        var_name='population',
        value_name='count'
    )
    
    melted_df['percentage'] = melted_df['count'] / melted_df['total_count'] * 100
    
    result_df = melted_df[[
        'sample', 
        'total_count', 
        'population', 
        'count', 
        'percentage'
    ]].sort_values(['sample', 'population'])
    
    return result_df.reset_index(drop=True)

def compare_treatment(db_name='loblow_bio.sqlite'):
    summary_df = create_summary(db_name)

    conn = sqlite3.connect(db_name)
    query = '''
        SELECT s.sample_id, t.response, s.sample_type
        FROM samples s
        JOIN treatments t ON s.sample_id = t.sample_id
        WHERE t.treatment = 'miraclib' AND s.sample_type = 'PBMC' 
    '''

    response_df = pd.read_sql(query, conn)
    conn.close()

    merged_df = summary_df.merge(response_df, left_on='sample', right_on='sample_id')
    merged_df = merged_df[merged_df['response'].isin(['yes', 'no'])]
    
    results = []
    
    for population in ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']:
        pop_df = merged_df[merged_df['population'] == population]
        
        # create boxplots
        fig = px.box(pop_df, x='response', y='percentage', 
                     color='response',
                     title=f'{population} percentage by response',
                     labels={'response': 'Response to Treatment', 'percentage': 'Percentage of Cells'},
                     hover_data=['sample'])
        fig.update_layout(showlegend=False)
        fig.write_html(f'{population}_response_comparison.html')
        print(f'Saved plot for {population} as {population}_response_comparison.html')
        
        # do statistical testing
        responders = pop_df[pop_df['response'] == 'yes']['percentage']
        non_responders = pop_df[pop_df['response'] == 'no']['percentage']
        
        if len(responders) > 1 and len(non_responders) > 1:
            stat, p = stats.mannwhitneyu(responders, non_responders)
            mean_res = np.mean(responders)
            mean_nonres = np.mean(non_responders)
            results.append({
                'population': population,
                'mean_responders': mean_res,
                'mean_non_responders': mean_nonres,
                'mean_difference': mean_res - mean_nonres,
                'p_value': p,
                'significant': p < 0.05
            })
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    return results_df

def analyze_baseline_samples(db_name='loblow_bio.sqlite'):
    conn = sqlite3.connect(db_name)
    query = '''
    SELECT 
        s.sample_id,
        s.subject_id,
        sub.project,
        sub.sex,
        t.response,
        t.b_cell,
        t.cd8_t_cell,
        t.cd4_t_cell,
        t.nk_cell,
        t.monocyte
    FROM samples s
    JOIN treatments t ON s.sample_id = t.sample_id
    JOIN subjects sub ON s.subject_id = sub.subject_id
    WHERE s.sample_type = 'PBMC' 
        AND s.time_from_treatment_start = 0
        AND t.treatment = 'miraclib'
        AND sub.condition = 'melanoma'
    '''
    baseline_df = pd.read_sql(query, conn)
    conn.close()
    
    if baseline_df.empty:
        print('No baseline PBMC samples found for melanoma patients treated with miraclib.')
        return None
    
    summary = {
        'projects': baseline_df['project'].value_counts().to_dict(),
        'response_counts': baseline_df['response'].value_counts().to_dict(),
        'sex_counts': baseline_df['sex'].value_counts().to_dict(),
        'total_samples': len(baseline_df),
        'total_subjects': baseline_df['subject_id'].nunique()
    }
    
    # create charts
    if summary['projects']:
        fig1 = px.bar(
            x=list(summary['projects'].keys()), 
            y=list(summary['projects'].values()),
            labels={'x': 'Project', 'y': 'Number of Samples'},
            title='Sample Distribution by Project'
        )
        fig1.write_html('project_distribution.html')
    
    if summary['response_counts']:
        fig2 = px.bar(
            x=list(summary['response_counts'].keys()), 
            y=list(summary['response_counts'].values()),
            labels={'x': 'Response', 'y': 'Number of Subjects'},
            title='Response Distribution'
        )
        fig2.write_html('response_distribution.html')
    
    if summary['sex_counts']:
        fig3 = px.bar(
            x=list(summary['sex_counts'].keys()), 
            y=list(summary['sex_counts'].values()),
            labels={'x': 'Sex', 'y': 'Number of Subjects'},
            title='Sex Distribution'
        )
        fig3.write_html('sex_distribution.html')
    
    print('Saved visualization files:')
    print('- project_distribution.html')
    print('- response_distribution.html')
    print('- sex_distribution.html')
    
    return summary