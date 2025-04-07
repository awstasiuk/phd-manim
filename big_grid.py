from manim import *

import rustworkx as rx
from math import ceil, floor
from numpy.random import rand
import pickle


def grid_graph_2d(L):
    r"""
    Returns a 2d square lattice where each noce is labeled by a spatial
    location, stored as a tuple of integers, (a,b)
    """
    G = rx.PyGraph()
    G.add_nodes_from([(i, j) for j in range(L) for i in range(L)])
    G.add_edges_from(
        [(i + j * L, i + 1 + j * L, None) for j in range(L) for i in range(L - 1)]
    )
    G.add_edges_from(
        [(i + j * L, i + (j + 1) * L, None) for j in range(L - 1) for i in range(L)]
    )
    return G


class BigGrid(Scene):
    def construct(self):
        L = 15
        G = grid_graph_2d(L)
        x0 = floor(L / 2)
        y0 = floor(L / 2) + 0.5
        scale = 2.5

        title = Text(f"Square Lattice, L={L}")
        title.to_edge(UP)
        self.play(Write(title))

        nodes = VGroup()
        for node in G.nodes():
            dot = Dot(
                point=[(node[0] - x0) / scale, (node[1] - y0) / scale, 0],
                radius=0.08,
                color=PURE_RED,
            )
            dot.z_index = 2
            nodes.add(dot)

        self.play(*[Create(dot) for dot in nodes], run_time=1)
        # self.play(Wait(), run_time=2)

        edges = VGroup()
        node_lst = G.nodes()
        for edge in G.edge_list():
            line = Line(
                start=[
                    (node_lst[edge[0]][0] - x0) / scale,
                    (node_lst[edge[0]][1] - y0) / scale,
                    0,
                ],
                end=[
                    (node_lst[edge[1]][0] - x0) / scale,
                    (node_lst[edge[1]][1] - y0) / scale,
                    0,
                ],
            )
            line.z_index = 0
            edges.add(line)
        self.play(*[Create(line) for line in edges], run_time=1)

        self.play(FadeOut(title))
        text = Text("Edge Acceptance Probability: p=.525")
        text.to_edge(UP)
        self.play(Write(text))

        # Now we cut edges!
        p = 0.525
        try:
            marked_edges_idxs = pickle.load(open("indices_to_cut_BIG.dat", "rb"))
        except (OSError, IOError) as e:
            marked_edges_idxs = [edge for edge in G.edge_indices() if p < rand()]
            with open("indices_to_cut_BIG.dat", "wb") as fi:
                pickle.dump(marked_edges_idxs, fi)

        marked_edges = [G.edge_list()[idx] for idx in marked_edges_idxs]
        cuts = VGroup()
        for edge_idx in marked_edges_idxs:
            cuts.add(edges[edge_idx])
        self.play(*[FadeOut(cuts)])

        G.remove_edges_from(marked_edges)
        comps = rx.connected_components(G)
        distro = [len(comp) for comp in comps]
        largest_local = np.max(distro)
        ll_idx = np.argmax(distro)

        largest_subgraph = list(comps[ll_idx])
        largest_sg_locs = [G[idx] for idx in largest_subgraph]

        largest_connected = VGroup()
        for node in nodes:
            if (
                (
                    int((node.get_center()[0] * scale + x0)),
                    int((node.get_center()[1] * scale + y0)),
                )
            ) in largest_sg_locs:
                largest_connected.add(node)

        self.play(Wait(run_time=1))

        self.play(FadeOut(text))
        text1 = Text("'Infinite' Subgraph")
        text1.to_edge(UP)
        self.play(Write(text1))

        self.play(
            *[
                Indicate(dot, color=PURE_BLUE, scale_factor=1.5)
                for dot in largest_connected
            ],
            run_time=5,
        )

        self.play(FadeOut(text1))
        text2 = Text("Random Walks")
        text2.to_edge(UP)
        self.play(Write(text2))

        n_points = 10
        origins = [
            G.node_indexes()[round(rand() * (L**2 - 1))] for _ in range(n_points)
        ]

        v1_list = origins
        self.play(*[nodes[v1].animate.set_color(YELLOW) for v1 in v1_list])
        neighbor_lists = [list(G.neighbors(v1)) for v1 in v1_list]
        for node, neighbors in zip(v1_list, neighbor_lists):
            if len(neighbors) == 0:
                v1_list.remove(node)

        steps = 100
        for _ in range(steps):
            neighbor_lists = [list(G.neighbors(v1)) for v1 in v1_list]
            v2_list = [
                neighbors[int(rand() * (len(neighbors)))]
                for neighbors in neighbor_lists
            ]
            v1_anims = [nodes[v1].animate.set_color(PURE_RED) for v1 in v1_list]
            v2_anims = [nodes[v2].animate.set_color(YELLOW) for v2 in v2_list]
            anims = v1_anims + v2_anims
            self.play(
                *anims,
                runtime=0.05,
                lag_ratio=0.75,
            )
            v1_list = v2_list

        final = v1_list
