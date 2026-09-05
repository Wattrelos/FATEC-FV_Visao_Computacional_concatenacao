#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FATEC - Faculdade de Tecnologia
Disciplina: Visão Computacional
Projeto: Concatenação de Imagens com OpenCV e NumPy

Este programa demonstra como manipular e unir duas imagens utilizando técnicas
de redimensionamento com preservação de aspecto (aspect ratio) e concatenação de matrizes:
  1. Concatenação Horizontal (cv2.hconcat) -> Requer que as alturas sejam iguais.
  2. Concatenação Vertical (cv2.vconcat)   -> Requer que as larguras sejam iguais.
"""

import os
import sys
import argparse
from typing import Tuple, Optional
import cv2
import numpy as np

# Configurações padrão
CAMINHO_PADRAO_IMG1 = "assets/cat_1.jpg"
CAMINHO_PADRAO_IMG2 = "assets/cat_2.jpg"
CAMINHO_SAIDA_PADRAO = "assets/resultado_concatenado.jpg"
NOME_JANELA = "Visao Computacional - Concatenacao de Imagens (FATEC-FV)"


def carregar_imagem(caminho: str) -> Optional[np.ndarray]:
    """
    Carrega uma imagem a partir do caminho de arquivo informado.

    Args:
        caminho: Caminho relativo ou absoluto do arquivo de imagem.

    Returns:
        np.ndarray da imagem em formato BGR ou None caso o carregamento falhe.
    """
    if not os.path.exists(caminho):
        print(f"[AVISO] Arquivo não encontrado: '{caminho}'")
        return None

    imagem = cv2.imread(caminho)
    if imagem is None:
        print(f"[ERRO] Não foi possível decodificar o arquivo de imagem: '{caminho}'")
    return imagem


def criar_imagens_demonstracao() -> Tuple[np.ndarray, np.ndarray]:
    """
    Gera duas imagens sintéticas coloridas de demonstração caso nenhum arquivo
    seja encontrado em disco. Útil para testes automatizados e fallback.

    Returns:
        Tupla com (img1, img2) em matrizes NumPy uint8.
    """
    print("[INFO] Gerando imagens sintéticas de demonstração...")

    # Imagem 1: (altura=400, largura=600), com gradiente azul/verde e formas
    img1 = np.zeros((400, 600, 3), dtype=np.uint8)
    for y in range(400):
        for x in range(600):
            img1[y, x] = [int(255 * (x / 600)), int(200 * (y / 400)), 80]
    cv2.putText(img1, "Imagem 1 (400x600)", (40, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(img1, (480, 200), 50, (0, 255, 255), -1)

    # Imagem 2: (altura=500, largura=500), com gradiente vermelho/roxo e formas
    img2 = np.zeros((500, 500, 3), dtype=np.uint8)
    for y in range(500):
        for x in range(500):
            img2[y, x] = [80, int(150 * (1 - y / 500)), int(255 * (x / 500))]
    cv2.putText(img2, "Imagem 2 (500x500)", (30, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img2, (320, 180), (450, 310), (0, 200, 255), -1)

    return img1, img2


def redimensionar_para_mesma_altura(imagem: np.ndarray, altura_alvo: int) -> np.ndarray:
    """
    Redimensiona uma imagem para que ela possua a altura especificada,
    preservando rigorosamente a sua proporção de aspecto (aspect ratio).

    Fórmula:
        fator_escala = altura_alvo / altura_original
        nova_largura = round(largura_original * fator_escala)

    Args:
        imagem: Matriz NumPy da imagem de entrada.
        altura_alvo: Nova altura desejada em pixels.

    Returns:
        Imagem redimensionada com altura igual a altura_alvo.
    """
    altura_orig, largura_orig = imagem.shape[:2]
    if altura_orig == altura_alvo:
        return imagem.copy()

    fator = altura_alvo / float(altura_orig)
    nova_largura = max(1, int(round(largura_orig * fator)))
    return cv2.resize(imagem, (nova_largura, altura_alvo), interpolation=cv2.INTER_AREA if fator < 1.0 else cv2.INTER_LINEAR)


def redimensionar_para_mesma_largura(imagem: np.ndarray, largura_alvo: int) -> np.ndarray:
    """
    Redimensiona uma imagem para que ela possua a largura especificada,
    preservando rigorosamente a sua proporção de aspecto (aspect ratio).

    Fórmula:
        fator_escala = largura_alvo / largura_original
        nova_altura  = round(altura_original * fator_escala)

    Args:
        imagem: Matriz NumPy da imagem de entrada.
        largura_alvo: Nova largura desejada em pixels.

    Returns:
        Imagem redimensionada com largura igual a largura_alvo.
    """
    altura_orig, largura_orig = imagem.shape[:2]
    if largura_orig == largura_alvo:
        return imagem.copy()

    fator = largura_alvo / float(largura_orig)
    nova_altura = max(1, int(round(altura_orig * fator)))
    return cv2.resize(imagem, (largura_alvo, nova_altura), interpolation=cv2.INTER_AREA if fator < 1.0 else cv2.INTER_LINEAR)


def concatenar_horizontal(imagem1: np.ndarray, imagem2: np.ndarray) -> np.ndarray:
    """
    Realiza a concatenação horizontal de duas imagens.
    Para concatenar lado a lado, ambas as matrizes precisam ter a mesma altura (número de linhas).
    A primeira imagem é redimensionada proporcionalmente para a altura da segunda imagem.

    Args:
        imagem1: Primeira imagem (lado esquerdo).
        imagem2: Segunda imagem (lado direito - referência de altura).

    Returns:
        Matriz concatenada com shape (altura2, nova_largura1 + largura2, canais).
    """
    altura2 = imagem2.shape[0]
    img1_redim = redimensionar_para_mesma_altura(imagem1, altura2)
    return cv2.hconcat([img1_redim, imagem2])


def concatenar_vertical(imagem1: np.ndarray, imagem2: np.ndarray) -> np.ndarray:
    """
    Realiza a concatenação vertical de duas imagens.
    Para empilhar imagens verticalmente, ambas as matrizes precisam ter a mesma largura (colunas).
    A primeira imagem é redimensionada proporcionalmente para a largura da segunda imagem.

    Args:
        imagem1: Primeira imagem (topo).
        imagem2: Segunda imagem (base - referência de largura).

    Returns:
        Matriz concatenada com shape (nova_altura1 + altura2, largura2, canais).
    """
    largura2 = imagem2.shape[1]
    img1_redim = redimensionar_para_mesma_largura(imagem1, largura2)
    return cv2.vconcat([img1_redim, imagem2])


def desenhar_rodape_informativo(imagem: np.ndarray, modo_atual: str) -> np.ndarray:
    """
    Desenha uma barra informativa inferior (HUD) com instruções de teclado e modo atual.

    Args:
        imagem: Imagem base para receber o overlay.
        modo_atual: Identificador do modo ("horizontal" ou "vertical").

    Returns:
        Nova imagem contendo a barra de informações.
    """
    saida = imagem.copy()
    h, w = saida.shape[:2]
    altura_barra = 36

    # Cria barra translúcida escura no rodapé
    overlay = saida.copy()
    cv2.rectangle(overlay, (0, h - altura_barra), (w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.75, saida, 0.25, 0, saida)

    texto = f"Modo: {modo_atual.upper()}  |  [H] Horizontal  [V] Vertical  [S] Salvar  [Q/ESC] Sair"
    cv2.putText(saida, texto, (15, h - 11), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    return saida


def obter_argumentos() -> argparse.Namespace:
    """Configura e processa os argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="FATEC-FV: Concatenação de Imagens em Visão Computacional com OpenCV"
    )
    parser.add_argument(
        "--img1", "-i1",
        default=CAMINHO_PADRAO_IMG1,
        help=f"Caminho para a primeira imagem (padrão: {CAMINHO_PADRAO_IMG1})"
    )
    parser.add_argument(
        "--img2", "-i2",
        default=CAMINHO_PADRAO_IMG2,
        help=f"Caminho para a segunda imagem (padrão: {CAMINHO_PADRAO_IMG2})"
    )
    parser.add_argument(
        "--modo", "-m",
        choices=["horizontal", "vertical", "ambos"],
        default="horizontal",
        help="Modo de concatenação inicial: 'horizontal' (padrão), 'vertical' ou 'ambos'"
    )
    parser.add_argument(
        "--salvar", "-s",
        action="store_true",
        help="Salva automaticamente o resultado em disco ao executar"
    )
    parser.add_argument(
        "--saida", "-o",
        default=CAMINHO_SAIDA_PADRAO,
        help=f"Caminho de destino do arquivo salvo (padrão: {CAMINHO_SAIDA_PADRAO})"
    )
    parser.add_argument(
        "--sem-janela",
        action="store_true",
        help="Executa em modo não-interativo (sem abrir janela gráfica), ideal para testes em lote"
    )
    return parser.parse_args()


def main():
    """Função principal que orquestra o carregamento, concatenação e interação."""
    args = obter_argumentos()

    print("=" * 68)
    print(" FATEC-FV - Visão Computacional: Concatenação de Imagens")
    print("=" * 68)

    # 1. Carregar imagens do disco
    print(f"[*] Carregando Imagem 1: '{args.img1}'...")
    imagem1 = carregar_imagem(args.img1)

    print(f"[*] Carregando Imagem 2: '{args.img2}'...")
    imagem2 = carregar_imagem(args.img2)

    # 2. Verificar se as imagens foram carregadas corretamente ou usar fallback
    if imagem1 is None or imagem2 is None:
        print("[!] Não foi possível carregar uma ou ambas as imagens especificadas.")
        print("[!] Utilizando imagens sintéticas de demonstração para continuar.")
        imagem1, imagem2 = criar_imagens_demonstracao()

    # Exibir informações das dimensões originais
    h1, w1 = imagem1.shape[:2]
    h2, w2 = imagem2.shape[:2]
    print(f"[OK] Imagem 1 carregada: {w1}x{h1} px (Largura x Altura), {imagem1.shape[2]} canais")
    print(f"[OK] Imagem 2 carregada: {w2}x{h2} px (Largura x Altura), {imagem2.shape[2]} canais")
    print("-" * 68)

    # Pré-computar ambos os modos
    resultado_horizontal = concatenar_horizontal(imagem1, imagem2)
    hh, wh = resultado_horizontal.shape[:2]
    print(f"[*] Concatenação Horizontal gerada: {wh}x{hh} px")

    resultado_vertical = concatenar_vertical(imagem1, imagem2)
    hv, wv = resultado_vertical.shape[:2]
    print(f"[*] Concatenação Vertical gerada:   {wv}x{hv} px")
    print("-" * 68)

    # Salvar automaticamente caso solicitado via CLI
    if args.salvar:
        caminho_salvar = args.saida
        os.makedirs(os.path.dirname(caminho_salvar) or ".", exist_ok=True)
        img_para_salvar = resultado_horizontal if args.modo != "vertical" else resultado_vertical
        sucesso = cv2.imwrite(caminho_salvar, img_para_salvar)
        if sucesso:
            print(f"[+] Imagem salva com sucesso em: '{caminho_salvar}'")
        else:
            print(f"[ERRO] Falha ao salvar imagem em: '{caminho_salvar}'")

    # Se modo não-interativo, finaliza aqui
    if args.sem_janela:
        print("[*] Execução em modo não-interativo finalizada.")
        return

    # Loop de visualização e interatividade
    modo_atual = "vertical" if args.modo == "vertical" else "horizontal"
    print("\n[Instruções de Teclado]")
    print("  [H]     -> Visualizar Concatenação Horizontal")
    print("  [V]     -> Visualizar Concatenação Vertical")
    print("  [S]     -> Salvar o resultado atual em disco")
    print("  [Q/ESC] -> Encerrar a aplicação\n")

    # Criar janela com propriedade normal para permitir redimensionamento caso a tela seja menor
    cv2.namedWindow(NOME_JANELA, cv2.WINDOW_NORMAL)

    while True:
        if modo_atual == "horizontal":
            # Desenha o rodape informativo na imagem horizontal
            tela = desenhar_rodape_informativo(resultado_horizontal, "horizontal")
        else:
            # Desenha o rodape informativo na imagem vertical
            tela = desenhar_rodape_informativo(resultado_vertical, "vertical")

        cv2.imshow(NOME_JANELA, tela)
        # Aguarda por 50ms por uma tecla e filtra apenas os 8 bits inferiores (ASCII) para evitar problemas com caracteres estendidos e teclas especiais.
        tecla = cv2.waitKey(50) & 0xFF

        # Sair: 'q', 'Q' ou tecla ESC (27)
        if tecla in [ord('q'), ord('Q'), 27]:
            print("[*] Encerrando aplicativo...")
            break
        # Alternar para Horizontal: 'h' ou 'H'
        elif tecla in [ord('h'), ord('H')]:
            if modo_atual != "horizontal":
                modo_atual = "horizontal"
                print("[*] Modo alterado para: HORIZONTAL")
        # Alternar para Vertical: 'v' ou 'V'
        elif tecla in [ord('v'), ord('V')]:
            if modo_atual != "vertical":
                modo_atual = "vertical"
                print("[*] Modo alterado para: VERTICAL")
        # Salvar: 's' ou 'S'
        elif tecla in [ord('s'), ord('S')]:
            nome_arquivo = f"assets/resultado_{modo_atual}.jpg"
            img_salvar = resultado_horizontal if modo_atual == "horizontal" else resultado_vertical
            cv2.imwrite(nome_arquivo, img_salvar)
            print(f"[+] Imagem ({modo_atual}) salva com sucesso em: '{nome_arquivo}'")

    # Fecha todas as janelas do OpenCV, liberando memória e recursos do sistema operacional
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
