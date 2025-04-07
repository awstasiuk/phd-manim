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


class PercAnim(Scene):
    def construct(self):
        L = 7
        G = grid_graph_2d(L)
        x0 = floor(L / 2)
        y0 = floor(L / 2) + 0.5

        title = Text(f"Square Lattice, L={L}")
        title.to_edge(UP)
        self.play(Write(title))

        nodes = VGroup()
        for node in G.nodes():
            dot = Dot(
                point=[node[0] - x0, node[1] - y0, 0],
                radius=0.15,
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
                start=[node_lst[edge[0]][0] - x0, node_lst[edge[0]][1] - y0, 0],
                end=[node_lst[edge[1]][0] - x0, node_lst[edge[1]][1] - y0, 0],
            )
            line.z_index = 0
            edges.add(line)
        self.play(*[Create(line) for line in edges], run_time=1)

        self.play(FadeOut(title))
        text = Text("Edge Acceptance Probability: p=.55")
        text.to_edge(UP)
        self.play(Write(text))

        # Now we cut edges!
        p = 0.55
        try:
            marked_edges_idxs = pickle.load(open("indices_to_cut.dat", "rb"))
        except (OSError, IOError) as e:
            marked_edges_idxs = [edge for edge in G.edge_indices() if p < rand()]
            with open("indices_to_cut.dat", "wb") as fi:
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
                node.get_center()[0] + x0,
                node.get_center()[1] + y0,
            ) in largest_sg_locs:
                largest_connected.add(node)

        self.play(FadeOut(text))
        text1 = Text("'Infinite' Subgraph")
        text1.to_edge(UP)
        self.play(Write(text1))

        # Replace their color with Blue
        self.play(
            *[dot.animate.set_color(PURE_BLUE) for dot in largest_connected],
            run_time=3,
        )

        self.play(
            *[
                Indicate(dot, color=PURE_BLUE, scale_factor=1.5)
                for dot in largest_connected
            ],
            run_time=2,
        )

        self.play(Wait(run_time=1))

        # pick two nodes in the largest cluster and find a shortest bath between them
        # each path here is technically unique
        # v1 = largest_subgraph[round(rand() * largest_local)]
        # v2 = largest_subgraph[round(rand() * largest_local)]
        v1 = 13
        v2 = 45
        valid_paths = rx.all_shortest_paths(G, v1, v2)
        path = valid_paths[0]

        def path_to_chk_pt(G, path):
            return [np.array(G[idx] + (0,)) - np.array([x0, y0, 0]) for idx in path]

        def line_segment_highlight(chk_pts, dt=1):
            highlights = VGroup()
            for ptA, ptB in zip(chk_pts[0:-1], chk_pts[1:]):
                bold_line = Line(
                    start=ptA,
                    end=ptB,
                    color=YELLOW,
                    stroke_width=12,
                )
                highlights.add(bold_line)
                # self.play(
                #    Create(bold_line, lag_ratio=0, rate_function=linear),
                #    run_time=dt,
                #    lag_ratio=0,
                # )
            self.play(
                Succession(
                    *[Create(line, rate_func=linear) for line in highlights],
                    lag_ratio=0.75,
                    run_time=len(highlights),
                )
            )

            return highlights

        self.play(FadeOut(text1))
        text2 = Text("Conductivity Dominated by Shortest Path")
        text2.to_edge(UP)
        self.play(Write(text2))

        # Highlight the points indicated by graph indices v1 and v2
        end_pts = VGroup()
        end_pts.add(nodes[v1])
        end_pts.add(nodes[v2])
        self.play(Indicate(end_pts, color=YELLOW, scale_factor=1.5), run_time=1)
        self.play(
            *[dot.animate.set_color(YELLOW) for dot in end_pts],
            run_time=1,
        )

        path_highlight = line_segment_highlight(path_to_chk_pt(G, path), dt=1)
