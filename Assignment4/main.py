import pandas as pd













def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df = pd.read_csv("rag_sample_queries_candidates.csv")

    #query_id,query_text,candidate_id,candidate_text,baseline_rank,baseline_score,gold_label


    for i in range(len(df)):
        print(df['query_text'][i])







if __name__ == '__main__':
    main()
