from TracerouteProcessor import TracerouteProcessor

if __name__ == "__main__":
    tp = TracerouteProcessor()

    fake_traceroutes = [
        [["IP1"], ["IP2a", "IP2b"], ["IP3"]],
        [["IP1"], ["IP2"]]
    ]

    tp.process_traceroutes(fake_traceroutes)
    print(tp.get_adjacency_list())

    # fake_traceroutes = [
    #     [["IP3"], ["IP4"]]
    # ]
    tp.process_traceroutes(fake_traceroutes)



    print(tp.get_adjacency_list())