#<><><><><><><>< DatasetMangler ><><><><><><><><>
class DatasetMangler:

    def __init__(self):
        self.logger = logging.getLogger("DatasetMangler")
        self.cwd = os.path.abspath(os.getcwd())
        self.fileName = None

    def downloadGitTarball(self, url):
    df_ger = pd.read_csv (r'/Users/Florian/covid19_GER_RKI_datadifference/JHU_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
    df_ger = df_ger[ df_ger["Country/Region"] == "Germany" ]

    df_re = pd.read_csv(r'/Users/Florian/covid19_GER_RKI_datadifference/JHU_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
    df_re_ger = df_re[df_re["Country/Region"] == "Germany"]
    df_ger = df_ger.append(df_re_ger)

    df_de = pd.read_csv(r'/Users/Florian/covid19_GER_RKI_datadifference/JHU_data/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
    df_de_ger = df_de[df_de["Country/Region"] == "Germany"]
    df = df_ger.append(df_de_ger)
    print(df)

    df.columns.values[0] = 'Type'
    df = df.assign(Type = ("Confirmed", "Recovered", "Deaths"))
    df = df.drop(['Lat', 'Long'], 1)
    print(df)

    df.to_csv(csv_JHU, encoding='utf-8', index=False)

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    data = DatasetDownloader()
    data.downloadGitTarball(JHU_CSSE_REPO)
    data.unzipTarball()
