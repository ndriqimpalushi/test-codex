import requests
import time

# Uniswap V2 subgraph endpoint
UNISWAP_V2_SUBGRAPH = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

# Volume threshold in USD
VOLUME_THRESHOLD = 1_000_000  # 1M USD

QUERY = """
query ($lastId: String) {
  pairs(first: 100, orderBy: createdAtTimestamp, orderDirection: desc, where: {id_gt: $lastId}) {
    id
    token0 { id symbol name }
    token1 { id symbol name }
    volumeUSD
  }
}
"""


def fetch_new_pairs(last_id="0"):
    response = requests.post(
        UNISWAP_V2_SUBGRAPH,
        json={"query": QUERY, "variables": {"lastId": last_id}},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data["data"]["pairs"]


def monitor():
    last_id = "0"
    print("Starting monitoring loop. Press Ctrl+C to exit.")
    while True:
        try:
            pairs = fetch_new_pairs(last_id)
            for pair in pairs:
                last_id = pair["id"]
                volume = float(pair.get("volumeUSD", 0))
                if volume >= VOLUME_THRESHOLD:
                    token0 = pair["token0"]["symbol"]
                    token1 = pair["token1"]["symbol"]
                    print(
                        f"High volume pair detected: {token0}/{token1} volumeUSD={volume:.2f}"
                    )
        except Exception as e:
            print("Error fetching pairs:", e)

        time.sleep(30)


if __name__ == "__main__":
    monitor()
