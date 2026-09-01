"""Gera o DFD da API em `others/dfd.png`.

Executar da raiz do repositório:

    python others/generate_dfd.py

O diagrama e a matriz CIA correspondente estão descritos em `others/dfd-and-cia.md`.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

SAIDA = Path(__file__).resolve().parent / "dfd.png"

AZUL = "#2F5C8F"
AZUL_CLARO = "#DCE7F3"
VERDE = "#3D7A57"
VERDE_CLARO = "#DCEDE2"
LARANJA = "#B26A2B"
LARANJA_CLARO = "#F7E5D0"
VERMELHO = "#B03A34"
CINZA = "#5B6068"


def entidade_externa(ax, x, y, largura, altura, titulo, subtitulo):
    ax.add_patch(
        Rectangle((x, y), largura, altura, facecolor=AZUL_CLARO, edgecolor=AZUL, linewidth=2.2)
    )
    ax.text(x + largura / 2, y + altura * 0.62, titulo, ha="center", va="center",
            fontsize=11, fontweight="bold", color=AZUL)
    ax.text(x + largura / 2, y + altura * 0.28, subtitulo, ha="center", va="center",
            fontsize=8.5, color=CINZA)


def processo(ax, x, y, raio, numero, titulo, subtitulo):
    """Processo na notação de bolha. O subtítulo fica FORA do círculo, logo abaixo."""
    ax.add_patch(Circle((x, y), raio, facecolor=VERDE_CLARO, edgecolor=VERDE, linewidth=2.2))
    ax.text(x, y + raio * 0.34, numero, ha="center", va="center",
            fontsize=9.5, fontweight="bold", color=VERDE)
    ax.text(x, y - raio * 0.12, titulo, ha="center", va="center",
            fontsize=10, fontweight="bold", color="#1D1D1D")
    ax.text(x, y - raio - 0.24, subtitulo, ha="center", va="top", fontsize=7.8, color=CINZA,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.2})


def deposito(ax, x, y, largura, altura, identificador, titulo, subtitulo):
    """Depósito de dados na notação de Gane-Sarson: aberto à direita."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y), largura, altura,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            facecolor=LARANJA_CLARO, edgecolor=LARANJA, linewidth=1.8,
        )
    )
    ax.plot([x + 0.62, x + 0.62], [y, y + altura], color=LARANJA, linewidth=1.5)
    ax.text(x + 0.31, y + altura / 2, identificador, ha="center", va="center",
            fontsize=9, fontweight="bold", color=LARANJA)
    ax.text(x + 0.78, y + altura * 0.63, titulo, ha="left", va="center",
            fontsize=9, fontweight="bold", color="#1D1D1D")
    ax.text(x + 0.78, y + altura * 0.28, subtitulo, ha="left", va="center",
            fontsize=7.6, color=CINZA)


def fluxo(ax, origem, destino, rotulo, rad=0.0, deslocamento=(0.0, 0.0), cor=AZUL, estilo="-"):
    ax.add_patch(
        FancyArrowPatch(
            origem, destino,
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>", mutation_scale=15,
            linewidth=1.5, color=cor, linestyle=estilo,
            shrinkA=3, shrinkB=3, zorder=3,
        )
    )
    meio_x = (origem[0] + destino[0]) / 2 + deslocamento[0]
    meio_y = (origem[1] + destino[1]) / 2 + deslocamento[1]
    ax.text(meio_x, meio_y, rotulo, ha="center", va="center", fontsize=7.4, color=cor,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 1.4},
            zorder=4)


def main() -> Path:
    fig, ax = plt.subplots(figsize=(17.5, 10.6))
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 10.6)
    ax.axis("off")

    ax.text(0.3, 10.15, "DFD — API de classificação de intenção de tickets (nível 1)",
            fontsize=16, fontweight="bold", color="#1D1D1D")
    ax.text(0.3, 9.78,
            "Projeto de Bloco TP1 — Anderson, Breno e Francisco  |  "
            "entradas, saídas e trust boundaries",
            fontsize=10, color=CINZA)

    # ---------------------------------------------------------------- boundaries
    ax.add_patch(
        Rectangle((3.9, 0.95), 8.35, 8.35, facecolor="#FBFCFD",
                  edgecolor=VERMELHO, linewidth=2.0, linestyle=(0, (7, 4)), zorder=0)
    )
    ax.text(4.05, 9.02, "TB1 — Fronteira Internet / API   (tudo à esquerda é NÃO CONFIÁVEL)",
            fontsize=9.5, fontweight="bold", color=VERMELHO)

    ax.add_patch(
        Rectangle((12.6, 0.95), 4.55, 8.35, facecolor="#FDFBF8",
                  edgecolor=VERMELHO, linewidth=2.0, linestyle=(0, (7, 4)), zorder=0)
    )
    ax.text(12.75, 9.02, "TB2 — Fronteira Aplicação / Segredos e artefatos",
            fontsize=9.5, fontweight="bold", color=VERMELHO)

    # ------------------------------------------------------------------ entidade
    entidade_externa(ax, 0.35, 4.35, 3.05, 1.5, "Administrador", "único usuário autorizado")

    # ------------------------------------------------------------------ processos
    processo(ax, 6.15, 8.10, 0.92, "P1", "GET /health", "rota pública, sem autenticação")
    processo(ax, 6.15, 5.55, 0.95, "P2", "POST /auth/token", "OAuth2PasswordRequestForm")
    processo(ax, 6.15, 2.70, 0.95, "P3", "POST /predict", "rota protegida por token")
    processo(ax, 10.30, 5.30, 1.02, "P4", "Segurança",
             "OAuth2PasswordBearer ·\nassina e valida o JWT")
    processo(ax, 10.30, 2.35, 0.92, "P5", "Predição", "stub determinístico")

    # ------------------------------------------------------------------ depósitos
    deposito(ax, 12.85, 7.15, 4.05, 0.95, "D1", "Credencial admin",
             "login/senha in-code (config.py)")
    deposito(ax, 12.85, 5.55, 4.05, 0.95, "D2", "Chave de assinatura JWT",
             "JWT_SECRET_KEY (variável de ambiente)")
    deposito(ax, 12.85, 3.35, 4.05, 0.95, "D3", "Dataset de tickets",
             "CSV com dados pessoais (nome, e-mail)")
    deposito(ax, 12.85, 1.70, 4.05, 0.95, "D4", "Modelo de ML",
             "artefato futuro — fora do escopo do TP1")

    # -------------------------------------------------------------------- fluxos
    fluxo(ax, (3.4, 5.42), (5.22, 5.72), "1  usuário + senha", rad=0.08, deslocamento=(0.05, 0.26))
    fluxo(ax, (5.28, 5.20), (3.4, 5.02), "2  JWT assinado\n(exp 30 min)", rad=0.08,
          deslocamento=(0.05, -0.46), cor=VERDE)
    fluxo(ax, (3.4, 4.72), (5.30, 3.10), "3  texto do ticket\n+ Bearer token", rad=-0.12,
          deslocamento=(-0.62, 0.26))
    fluxo(ax, (5.42, 2.30), (3.55, 4.32), "4  intenção JSON\n(sem eco do texto)", rad=-0.14,
          deslocamento=(-0.20, -0.58), cor=VERDE)
    fluxo(ax, (3.4, 5.98), (5.30, 7.72), "5  GET /health", rad=0.12, deslocamento=(-0.42, 0.24))
    fluxo(ax, (5.42, 8.52), (3.4, 6.28), '6  {"status":"ok"}', rad=0.12,
          deslocamento=(0.62, 0.34), cor=VERDE)

    fluxo(ax, (7.05, 5.95), (12.85, 7.35), "7  lê credencial", rad=0.05, deslocamento=(0, 0.30))
    fluxo(ax, (7.12, 5.35), (9.28, 5.10), "8  emitir token", rad=-0.06, deslocamento=(0, -0.28))
    fluxo(ax, (7.02, 3.12), (9.52, 4.48), "9  valida assinatura,\nexp e sub", rad=-0.22,
          deslocamento=(-0.36, 0.66))
    fluxo(ax, (9.45, 4.62), (7.05, 3.02), "10  identidade admin\nou 401", rad=-0.22,
          deslocamento=(0.34, -0.70), cor=VERDE)
    fluxo(ax, (11.34, 5.55), (12.85, 6.05), "11  lê chave", rad=-0.06, deslocamento=(0.05, 0.26))
    fluxo(ax, (7.10, 2.42), (9.40, 2.28), "12  texto validado", rad=-0.05, deslocamento=(0, -0.30))
    fluxo(ax, (11.22, 2.28), (12.85, 2.20), "13  (futuro)\ncarrega modelo", rad=0.0,
          deslocamento=(-0.38, 0.42), cor=CINZA, estilo=(0, (4, 3)))
    fluxo(ax, (14.20, 3.30), (14.20, 2.72), "14  (futuro) treino", rad=0.0,
          deslocamento=(1.15, 0.0), cor=CINZA, estilo=(0, (4, 3)))

    # ------------------------------------------------------------------- legenda
    ax.add_patch(Rectangle((0.35, 0.55), 3.05, 3.45, facecolor="white",
                           edgecolor="#C9CDD4", linewidth=1.2))
    ax.text(0.55, 3.72, "Legenda", fontsize=10, fontweight="bold", color="#1D1D1D")

    ax.add_patch(Rectangle((0.6, 3.15), 0.42, 0.26, facecolor=AZUL_CLARO,
                           edgecolor=AZUL, linewidth=1.6))
    ax.text(1.15, 3.28, "entidade externa", fontsize=8.2, va="center", color=CINZA)

    ax.add_patch(Circle((0.81, 2.78), 0.19, facecolor=VERDE_CLARO,
                        edgecolor=VERDE, linewidth=1.6))
    ax.text(1.15, 2.78, "processo", fontsize=8.2, va="center", color=CINZA)

    ax.add_patch(FancyBboxPatch((0.6, 2.15), 0.42, 0.26,
                                boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor=LARANJA_CLARO, edgecolor=LARANJA, linewidth=1.6))
    ax.text(1.15, 2.28, "depósito de dados", fontsize=8.2, va="center", color=CINZA)

    ax.plot([0.6, 1.02], [1.82, 1.82], color=VERMELHO, linewidth=2, linestyle=(0, (5, 3)))
    ax.text(1.15, 1.82, "trust boundary", fontsize=8.2, va="center", color=CINZA)

    ax.annotate("", xy=(1.02, 1.42), xytext=(0.6, 1.42),
                arrowprops={"arrowstyle": "-|>", "color": AZUL, "linewidth": 1.5})
    ax.text(1.15, 1.42, "entrada / requisição", fontsize=8.2, va="center", color=CINZA)

    ax.annotate("", xy=(1.02, 1.02), xytext=(0.6, 1.02),
                arrowprops={"arrowstyle": "-|>", "color": VERDE, "linewidth": 1.5})
    ax.text(1.15, 1.02, "saída / resposta", fontsize=8.2, va="center", color=CINZA)

    ax.annotate("", xy=(1.02, 0.72), xytext=(0.6, 0.72),
                arrowprops={"arrowstyle": "-|>", "color": CINZA, "linewidth": 1.5,
                            "linestyle": (0, (4, 3))})
    ax.text(1.15, 0.72, "fluxo futuro (fora do TP1)", fontsize=8.2, va="center", color=CINZA)

    # ---------------------------------------------------- nota sobre as fronteiras
    ax.text(
        4.05, 0.55,
        "TB1: toda entrada vinda do administrador é não confiável — exige TLS no ambiente "
        "publicado, validação Pydantic, autenticação JWT e limite de tamanho de payload.\n"
        "TB2: segredos (D1, D2) e artefatos (D3, D4) só podem ser lidos pelo processo da "
        "aplicação — exigem controle de acesso do sistema de arquivos, proibição em logs e "
        "verificação de integridade.",
        fontsize=8.4, color=VERMELHO, va="bottom",
    )

    fig.savefig(SAIDA, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return SAIDA


if __name__ == "__main__":
    caminho = main()
    print("DFD gerado em:", caminho)
