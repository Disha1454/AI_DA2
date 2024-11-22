import random

# Define the Bayesian Belief Network (BBN) as conditional probability tables
bbn = {
    "Rain": {
        True: 0.2,
        False: 0.8,
    },
    "Sprinkler": {
        True: {True: 0.01, False: 0.4},   # P(Sprinkler=True | Rain)
        False: {True: 0.99, False: 0.6},  # P(Sprinkler=False | Rain)
    },
    "GrassWet": {
        True: {True: 0.9, False: 0.8},    # P(GrassWet=True | Sprinkler)
        False: {True: 0.1, False: 0.2},   # P(GrassWet=False | Sprinkler)
    },
}

# Monte Carlo simulation function
def monte_carlo_inference(target, evidence, samples=10000):
    """
    Perform Monte Carlo simulation to estimate conditional probability.
    
    :param target: The target node to calculate probability for (e.g., "GrassWet").
    :param evidence: Dictionary of evidence nodes and their values (e.g., {"Rain": True}).
    :param samples: Number of random samples to generate.
    :return: Estimated probability of the target node being True.
    """
    count_target_true = 0
    count_valid_samples = 0

    for _ in range(samples):
        # Generate a random sample from the network
        sample = {}

        # Assign Rain based on its prior probability
        sample["Rain"] = random.random() < bbn["Rain"][True]

        # Assign Sprinkler based on conditional probability given Rain
        sample["Sprinkler"] = (
            random.random() < bbn["Sprinkler"][sample["Rain"]][True]
        )

        # Assign GrassWet based on conditional probability given Sprinkler
        sample["GrassWet"] = (
            random.random() < bbn["GrassWet"][sample["Sprinkler"]][True]
        )

        # Check if the sample matches the evidence
        if all(sample[node] == value for node, value in evidence.items()):
            count_valid_samples += 1

            # Check if the target node is True in valid samples
            if sample[target]:
                count_target_true += 1

    # Calculate conditional probability
    if count_valid_samples == 0:
        return 0  # Avoid division by zero if no samples match the evidence
    return count_target_true / count_valid_samples

# Example usage
if __name__ == "__main__":
    target_node = "GrassWet"
    evidence_nodes = {"Rain": True}
    num_samples = 10000

    probability = monte_carlo_inference(target_node, evidence_nodes, num_samples)
    print(f"P({target_node}=True | Evidence={evidence_nodes}) = {probability:.4f}")
