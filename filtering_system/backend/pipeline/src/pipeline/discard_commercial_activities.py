from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Load filtered suggestions
file_path = "../../data/post_external/filtered_suggested_activities.xlsx"
df_filtered = pd.read_excel(file_path)

# Load commercial activities from CSV
commercial_activities_path = "../../artifacts/commercial_activities.csv" 
df_commercial = pd.read_csv(commercial_activities_path, header=None, names=["name"])

# Encode commercial activities
commercial_list = df_commercial["name"].tolist()
commercial_embeddings = model.encode(commercial_list, convert_to_tensor=True, normalize_embeddings=True)

# Function to check duplicates
def check_duplicates(suggestions, threshold=0.60):
    filtered_activities = []
    discarded_activities = []

    for _, row in suggestions.iterrows():
        new_embedding = model.encode([row["name"] + " - " + row["description"]], convert_to_tensor=True, normalize_embeddings=True)
        similarity_scores = util.pytorch_cos_sim(new_embedding, commercial_embeddings)
        max_similarity, nearest_index = similarity_scores.max(dim=1)
        max_similarity = max_similarity.item()
        nearest_activity = commercial_list[nearest_index.item()]

        if max_similarity >= threshold:
            discarded_activities.append(row)
        else:
            filtered_activities.append(row)

    return pd.DataFrame(filtered_activities), pd.DataFrame(discarded_activities)

# Run duplicate detection against commercial activities
df_final, df_discarded_external = check_duplicates(df_filtered)

# Save outputs
final_output = "../../data/post_commercial_filter/filtered_suggested_activities.xlsx"
discarded_external_output = "../../data/post_commercial_filter/discarded_suggestions.xlsx"

df_final.to_excel(final_output, index=False)
df_discarded_external.to_excel(discarded_external_output, index=False)

