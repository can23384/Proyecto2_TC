import time
from copy import deepcopy
import matplotlib.pyplot as plt
import re

# GRAMÁTICA BASE 
grammar = {
    "S": [["NP", "VP"]],
    "VP": [["VP", "PP"], ["V", "NP"], ["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "PP": [["P", "NP"]],
    "NP": [["Det", "N"], ["he"], ["she"]],
    "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "P": [["in"], ["with"]],
    "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
    "Det": [["a"], ["the"]]
}


#SIMPLIFICACIÓN DE GRAMÁTICA
def remove_epsilon_productions(grammar):
    grammar = deepcopy(grammar)
    nullable = set()

    for head, bodies in grammar.items():
        for body in bodies:
            if body == ['ε'] or body == []:
                nullable.add(head)

    changed = True
    while changed:
        changed = False
        for head, bodies in grammar.items():
            for body in bodies:
                if all(symbol in nullable for symbol in body):
                    if head not in nullable:
                        nullable.add(head)
                        changed = True

    new_grammar = {}
    for head, bodies in grammar.items():
        new_bodies = []
        for body in bodies:
            if body != ['ε']:
                options = [[]]
                for symbol in body:
                    if symbol in nullable:
                        options = [opt + [symbol] for opt in options] + [opt for opt in options]
                    else:
                        options = [opt + [symbol] for opt in options]
                for opt in options:
                    if opt:
                        new_bodies.append(opt)
        new_grammar[head] = []
        for body in new_bodies:
            if body not in new_grammar[head]:
                new_grammar[head].append(body)
    return new_grammar


def remove_unit_productions(grammar):
    grammar = deepcopy(grammar)
    new_grammar = {}

    for head in grammar:
        new_grammar[head] = []

    for head in grammar:
        closure = {head}
        added = True
        while added:
            added = False
            for body in grammar[head]:
                if len(body) == 1 and body[0] in grammar:
                    B = body[0]
                    if B not in closure:
                        closure.add(B)
                        added = True
        for B in closure:
            for body in grammar[B]:
                if not (len(body) == 1 and body[0] in grammar):
                    if body not in new_grammar[head]:
                        new_grammar[head].append(body)
    return new_grammar


def remove_useless_symbols(grammar):
    grammar = deepcopy(grammar)

    generating = set()
    changed = True
    while changed:
        changed = False
        for head, bodies in grammar.items():
            for body in bodies:
                if all(symbol.islower() or symbol in generating for symbol in body):
                    if head not in generating:
                        generating.add(head)
                        changed = True

    grammar = {h: [b for b in bodies if all(s.islower() or s in generating for s in b)]
               for h, bodies in grammar.items() if h in generating}

    reachable = set(["S"])
    changed = True
    while changed:
        changed = False
        for head in list(reachable):
            for body in grammar.get(head, []):
                for symbol in body:
                    if symbol in grammar and symbol not in reachable:
                        reachable.add(symbol)
                        changed = True

    grammar = {h: [b for b in bodies] for h, bodies in grammar.items() if h in reachable}
    return grammar


def simplify_grammar(grammar):
    print("Simplificando gramática...")
    g1 = remove_epsilon_productions(grammar)
    g2 = remove_unit_productions(g1)
    g3 = remove_useless_symbols(g2)
    print("Gramática simplificada correctamente ✅\n")
    return g3


#CONVERSIÓN A FORMA NORMAL DE CHOMSKY
def convert_to_cnf(grammar):
    cnf = {}
    for head, bodies in grammar.items():
        cnf[head] = []
        for body in bodies:
            if len(body) == 1:
                cnf[head].append(body)
            elif len(body) == 2:
                cnf[head].append(body)
            else:
                prev = body[0]
                for i in range(1, len(body) - 1):
                    new_var = f"{head}_X{i}"
                    cnf[new_var] = [[prev, body[i]]]
                    prev = new_var
                cnf[head].append([prev, body[-1]])
    return cnf


# ALGORITMO CYK 
def cyk_algorithm(words, grammar):
    n = len(words)
    table = [[set() for _ in range(n)] for _ in range(n)]
    back = [[{} for _ in range(n)] for _ in range(n)]

    for i, word in enumerate(words):
        for head, bodies in grammar.items():
            for body in bodies:
                if len(body) == 1 and body[0] == word:
                    table[i][i].add(head)
                    back[i][i][head] = word

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for head, bodies in grammar.items():
                    for body in bodies:
                        if len(body) == 2:
                            B, C = body
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(head)
                                back[i][j][head] = ((B, i, k), (C, k + 1, j))
    return table, back



# CONSTRUCCIÓN Y DIBUJO DEL PARSE TREE 
def build_tree(back, i, j, symbol):
    if i == j:
        return (symbol, back[i][j][symbol])
    left, right = back[i][j][symbol]
    left_tree = build_tree(back, left[1], left[2], left[0])
    right_tree = build_tree(back, right[1], right[2], right[0])
    return (symbol, [left_tree, right_tree])


def draw_parse_tree(tree, filename="parse_tree", show=False):
    """Dibuja el árbol sintáctico usando matplotlib (sin Graphviz)."""
    nodes, edges, leaves_order = [], [], []

    def to_nodes_edges(t, depth=0):
        node_id = id(t)
        label = t[0]
        nodes.append((node_id, label, depth))
        if isinstance(t[1], str):  # hoja
            leaf_id = f"{node_id}_leaf"
            nodes.append((leaf_id, t[1], depth + 1))
            edges.append((node_id, leaf_id))
            leaves_order.append(leaf_id)
        else:
            left, right = t[1]
            left_id = to_nodes_edges(left, depth + 1)
            right_id = to_nodes_edges(right, depth + 1)
            edges.append((node_id, left_id))
            edges.append((node_id, right_id))
        return node_id

    to_nodes_edges(tree)
    x_leaf = {leaf: i for i, leaf in enumerate(leaves_order)}
    from collections import defaultdict
    children_map = defaultdict(list)
    for p, c in edges:
        children_map[p].append(c)
    pos = {}

    def compute_pos(node_id, depth):
        if node_id in x_leaf:
            pos[node_id] = (x_leaf[node_id], -depth)
            return pos[node_id][0]
        cs = children_map.get(node_id, [])
        xs = [compute_pos(c, depth + 1) for c in cs]
        x = sum(xs) / len(xs)
        pos[node_id] = (x, -depth)
        return x

    child_set = {c for _, c in edges}
    root_id = [nid for nid, _, _ in nodes if nid not in child_set and not str(nid).endswith("_leaf")][0]
    compute_pos(root_id, 0)

    fig, ax = plt.subplots(figsize=(max(6, len(leaves_order)*1.4), 5))
    ax.axis('off')
    for p, c in edges:
        (x1, y1), (x2, y2) = pos[p], pos[c]
        ax.plot([x1, x2], [y1, y2], color='black')
    for nid, label, depth in nodes:
        x, y = pos[nid]
        if str(nid).endswith("_leaf"):
            ax.text(x, y, label, ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.25", fc="white"))
        else:
            ax.text(x, y, label, ha='center', va='center',
                    bbox=dict(boxstyle="circle,pad=0.35", fc="lightblue"))
    ax.set_xlim(min(x for x,_ in pos.values())-1, max(x for x,_ in pos.values())+1)
    ax.set_ylim(min(y for _,y in pos.values())-1, max(y for _,y in pos.values())+1)
    outpath = f"{filename}.png"
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    print(f"🌳 Árbol sintáctico exportado en: {outpath}")



def safe_filename(sentence):
    base = re.sub(r'[^a-z0-9]+', '_', sentence.lower()).strip('_') or "parse_tree"
    return f"parse_tree_{base}"

def main():
    print("=== Algoritmo CYK - Reconocimiento de frases en inglés ===\n")
    sentence = input("Ingrese una frase en inglés (por ejemplo: 'She eats a cake with a fork'): ").strip()

    if not sentence:
        print("No ingresó ninguna frase. Saliendo...")
        return

    words = sentence.lower().replace(".", "").split()
    simplified = simplify_grammar(grammar)
    cnf = convert_to_cnf(simplified)

    start_time = time.time()
    table, back = cyk_algorithm(words, cnf)
    elapsed = time.time() - start_time

    if "S" in table[0][-1]:
        print(f"\n✅ '{sentence}' pertenece al lenguaje (tiempo: {elapsed:.6f}s)\n")
        tree = build_tree(back, 0, len(words) - 1, "S")
        filename = safe_filename(sentence)
        draw_parse_tree(tree, filename=filename)
    else:
        print(f"\n❌ '{sentence}' NO pertenece al lenguaje (tiempo: {elapsed:.6f}s)\n")



if __name__ == "__main__":
    main()
