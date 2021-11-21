import csv
import re
from utils import calculate_n_grams, calc_fq

if __name__ == "__main__":
    pattern = r'[0-9/\:\[\]\.\"\?\;\-\,\ ]'
    with open("../assets/train_text.txt", 'r', encoding="utf-8") as t_f:
        trained = bytes(re.sub(pattern, '', t_f.read().upper()), "utf-8")
    three_grams = calculate_n_grams(trained, 3)
    fq = list([calc_fq(trained, three_gram) for three_gram in three_grams])
    headers = ['n-gram', 'Frequency']
    with open('../assets/tri_grams_fq.csv', 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for key, value in frequency.items():
            writer.writerow([key, value])
