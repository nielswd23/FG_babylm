import random
import os

forms_path = "./fg-source-code-restore/data/brown_adam_full/brown_adam.forms.txt"
counts_path = "./fg-source-code-restore/data/brown_adam_full/brown_adam.counts.txt"

with open(forms_path, 'r') as file:
    forms = file.readlines()

with open(counts_path, 'r') as file:
    counts = file.readlines()

def sample(l_forms, l_counts, num_samples):
    zipped = list(zip(l_forms, l_counts))

    sampled = random.sample(zipped, num_samples)

    sampled_forms, sampled_counts = zip(*sampled)

    sampled_forms = list(sampled_forms)
    sampled_counts = list(sampled_counts)

    return sampled_forms, sampled_counts


# 10 samples
for i in range(1,11):
    folder_name = f"sample_{i}"
    os.makedirs(folder_name, exist_ok=True)


sampled_forms, sampled_counts = sample(forms, counts, 13500)