
def kmer_similarity(seq1: str, seq2: str, k: int = 6) -> dict:
    # Extract k-mers from both sequences
    kmers_seq1 = {seq1[i:i + k] for i in range(len(seq1) - k + 1)} if len(seq1) >= k else set()
    kmers_seq2 = {seq2[i:i + k] for i in range(len(seq2) - k + 1)} if len(seq2) >= k else set()
      # Find common k-mers
    common_kmers = kmers_seq1.intersection(kmers_seq2)

    denominator = max(len(kmers_seq1), len(kmers_seq2))
    # Calculate similarity score using Jaccard 
    similarity_score_jaccard = (
        len(common_kmers) / denominator if denominator != 0 else 0
    )

    return {
        "similarity_score_jaccard": similarity_score_jaccard,
        "common_kmers": list(common_kmers),
        "unique_kmers_seq1": list(kmers_seq1 - common_kmers),
        "unique_kmers_seq2": list(kmers_seq2 - common_kmers)
    }
