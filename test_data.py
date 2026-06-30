from data.analyzer import DataAnalyzer

analyzer = DataAnalyzer()

df = analyzer.load_file("healthcare_dataset.csv")

print(analyzer.get_summary(df))
