from datascraper.filters import filter_1, filter_2, filter_3


def process_data(input_data):
    # data = filter_1(input_data)
    data = filter_1(input_data)
    print(data)
    data = filter_2(data)
    print(data)
    data = filter_3(data)
    return data

if __name__ == "__main__":
    url = "https://www.mse.mk/mk/stats/symbolhistory/KMB"  #Input for option 1
    url_corrected = "https://www.mse.mk/en/stats/current-schedule"  #Input for option 2
    # data = process_data(url)  #OPTON 1
    data = process_data(url)    #OPTION 2

    #TODO
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSEDataAnalising.settings")
    # execute_from_command_line(sys.argv)


    # print(f"Total number of new companies: {len(data)}")
    # total_data = 0
    # for company_code, data_per_company in data:
    #     total_data += len(data_per_company)
    #     df = pd.DataFrame(data_per_company)
    #     df.to_csv(f'all_data/{company_code}.csv', index=False)
    #
    # print(f"Total number of new data scraped: {total_data} (rows)")