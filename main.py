from data_analysis import create_summary, compare_treatment, analyze_baseline_samples
from database_management import create_database, add_sample, remove_sample, load_data

def run_all_analyses():
    print("Generating summary table of cell population frequencies...")
    summary_table = create_summary()
    print("\nSummary table preview:")
    print(summary_table.head())
    
    print("\nComparing responders vs non-responders...")
    stats_results = compare_treatment()
    print("\nStatistical results:")
    print(stats_results)
    
    print("\nAnalyzing baseline PBMC samples...")
    baseline_summary = analyze_baseline_samples()
    print("\nBaseline sample summary:")
    print(baseline_summary)

def menu_options():
    print('1: Run all Analysis')
    print('2: Load Data')
    print('3: Add Sample')
    print('4: Remove Sample')
    print('5: Exit')
    
    while True:
        choice = input('Enter Choice (1-5): ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print('Invalid Input, Try Again\n\n\n')

if __name__ == "__main__":
    create_database()
    # tempory new sample (should be replaced with interface for the scientist)
    new_sample = {
        'project': 'prj1',
        'subject': 'sbj000',
        'condition': 'melanoma',
        'age': 57,
        'sex': 'M',
        'treatment': 'miraclib',
        'response': 'no',
        'sample': 'sample00000',
        'sample_type': 'PBMC',
        'time_from_treatment_start': 0,
        'b_cell': 10908,
        'cd8_t_cell': 24440,
        'cd4_t_cell': 20491,
        'nk_cell': 13864,
        'monocyte': 23511
    }
    # print option menu and call corresponding function (should be expanding for actual product with interactive interface and means of getting data)
    choice = menu_options()
    if choice == '1':
        run_all_analyses()
    elif choice == '2':
        load_data()
    elif choice == '3':
        add_sample(new_sample)
    elif choice == '4':
        remove_sample('sample00000')