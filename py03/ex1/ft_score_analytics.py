import sys


def ft_score_analytics() -> None:
    print("=== Player score analytics ===")
    if len(sys.argv) < 2:
        print("No scores provided. Usage: "
              "ft_score_analytics <score1> <score2> ...")
    else:
        score_list = []
        for score in sys.argv[1:]:
            try:
                score_list.append(int(score))
            except ValueError as e:
                print(f"Invalid score passed: {e}")
                sys.exit(1)
        print(f"Scores processed: {score_list}")
        print(f"Total players: {len(score_list)}")
        print(f"Total score: {sum(score_list)}")
        print(f"Low score: {min(score_list)}")
        print(f"High score: {max(score_list)}")
        print(f"Average score: {sum(score_list) / len(score_list)}")
        print(f"Score range: {max(score_list) - min(score_list)}")


if __name__ == "__main__":
    ft_score_analytics()
