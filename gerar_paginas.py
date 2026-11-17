"""Gera uma página por assunto a partir do index.html (20/10/2026).

Cada grupo de anúncio do Google aponta para a sua página. O visual e o conteúdo são os do index.html;
mudam só título, descrição, endereço canônico, H1, frase do topo, foto do topo e o interesse já marcado no formulário.
Sempre que o index.html mudar: python gerar_paginas.py (reescreve os .html e o sitemap.xml).
"""
import re, sys
from datetime import date

BASE = 'https://lp.ouzecv.com.br/'
FOTO_PADRAO = 'fachada-acm-clinica-maranatha'

PAGINAS = [
    dict(slug='fachada-comercial',
         titulo='Fachada Comercial para Lojas e Empresas no RS | OUZE',
         descricao='Fachada comercial, fachada de loja e fachada de empresa no RS: placa de fachada, ACM, letras-caixa e luminosos com projeto 3D, produção e instalação.',
         h1='Fachada comercial para lojas e empresas no RS',
         sub='Projeto 3D, produção e instalação de fachada de loja, fachada de empresa e placa de fachada, em ACM, letras-caixa e luminosos, para empresas de todo o RS.',
         foto=FOTO_PADRAO, alt='Fachada comercial em ACM colorida da Clínica Maranatha com letras-caixa, obra entregue pela OUZE',
         interesse='Fachada'),
    dict(slug='fachada-acm',
         titulo='Fachada em ACM e Placa de ACM para Empresas no RS | OUZE',
         descricao='Fachada em ACM, placa de ACM, painel e revestimento em ACM para lojas e empresas no RS, com projeto 3D, produção e instalação.',
         h1='Fachada em ACM para empresas no RS',
         sub='Placa de ACM, painel em ACM e revestimento em ACM com projeto 3D, produção e instalação, para lojas, clínicas e empresas de todo o RS.',
         foto=FOTO_PADRAO, alt='Fachada em ACM colorida da Clínica Maranatha com letras-caixa, obra entregue pela OUZE',
         interesse='Revestimento em ACM'),
    dict(slug='comunicacao-visual',
         titulo='Comunicação Visual para Empresas no RS | OUZE',
         descricao='Empresa de comunicação visual no RS com 25 anos de mercado: fachadas, ACM, letras-caixa, letreiros luminosos, totens e sinalização, do projeto 3D à instalação.',
         h1='Comunicação visual para empresas no RS',
         sub='Empresa de comunicação visual com 25 anos de mercado: projeto 3D, produção e instalação de fachadas, letras-caixa, luminosos, totens e sinalização para empresas de todo o RS.',
         foto=FOTO_PADRAO, alt='Fachada em ACM colorida da Clínica Maranatha com letras-caixa, obra de comunicação visual da OUZE',
         interesse=None),
    dict(slug='letra-caixa',
         titulo='Letra-Caixa para Fachadas no RS, com LED e em 3D | OUZE',
         descricao='Letra-caixa para fachada no RS: letra-caixa iluminada, letra-caixa com LED e letras em impressão 3D, com projeto 3D, produção e instalação.',
         h1='Letra-caixa para fachadas no RS',
         sub='Letra-caixa iluminada, letra-caixa com LED ou sem iluminação e letras em impressão 3D, com projeto 3D, produção e instalação para empresas de todo o RS.',
         foto='fachada-letra-caixa-vitrine-do-mar', alt='Fachada da peixaria Vitrine do Mar com letreiro em letra-caixa, obra entregue pela OUZE',
         interesse='Letra-caixa'),
    dict(slug='letreiro-luminoso',
         titulo='Letreiro Luminoso e Letreiro de LED para Empresas no RS | OUZE',
         descricao='Letreiro luminoso, letreiro de LED e painel luminoso para fachada no RS, com projeto 3D, produção e instalação.',
         h1='Letreiro luminoso para empresas no RS',
         sub='Letreiro luminoso, letreiro de LED e painel luminoso para fachada, com projeto 3D, produção e instalação para empresas de todo o RS.',
         foto='fachada-acm-pompeia-noite', alt='Fachada da loja Pompéia à noite com letreiro luminoso, obra entregue pela OUZE',
         interesse='Luminoso'),
    dict(slug='totem',
         titulo='Totem para Empresa, Totem Luminoso e Sinalização no RS | OUZE',
         descricao='Totem para empresa, totem luminoso, totem publicitário e totem de sinalização no RS, com projeto 3D, produção e instalação.',
         h1='Totem e sinalização para empresas no RS',
         sub='Totem para empresa, totem luminoso e totem de sinalização, com projeto 3D, produção e instalação para empresas de todo o RS.',
         foto='fachada-totem-oral-sin', alt='Totem da clínica Oral Sin na frente da fachada, obra entregue pela OUZE',
         interesse='Totem / sinalização'),
]


def troca(html, antigo, novo, n=1):
    achou = html.count(antigo)
    if achou != n:
        sys.exit('esperava %d ocorrência(s) e achei %d de: %s' % (n, achou, antigo[:90]))
    return html.replace(antigo, novo)


def gerar(base_html, p):
    h = base_html
    url = BASE + p['slug']
    h = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % p['titulo'], h, count=1)
    h = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + p['descricao'], h, count=1)
    h = troca(h, '<link rel="canonical" href="%s">' % BASE, '<link rel="canonical" href="%s">' % url)
    h = troca(h, '<meta property="og:url" content="%s">' % BASE, '<meta property="og:url" content="%s">' % url)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + p['titulo'], h, count=1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + p['descricao'], h, count=1)
    # H1 fixo no HTML (o script não troca quando há data-fixo)
    h = re.sub(r'<span id="heroKw">[^<]*</span>', '<span id="heroKw" data-fixo="1">%s</span>' % p['h1'], h, count=1)
    h = re.sub(r'(<p class="hero-sub">)[^<]*(</p>)', r'\g<1>' + p['sub'] + r'\g<2>', h, count=1)
    # foto do topo (figura e pré-carregamento)
    if p['foto'] != FOTO_PADRAO:
        h = troca(h, 'assets/img/%s-' % FOTO_PADRAO, 'assets/img/%s-' % p['foto'], h.count('assets/img/%s-' % FOTO_PADRAO))
    h = re.sub(r'(<figure class="hero-foto">.*?alt=")[^"]*', r'\g<1>' + p['alt'], h, count=1, flags=re.S)
    # interesse já marcado (o modal copia o formulário com o atributo)
    if p['interesse']:
        h = troca(h, '<option>%s</option>' % p['interesse'], '<option selected>%s</option>' % p['interesse'])
    return h


def main():
    base_html = open('index.html', encoding='utf-8').read()
    # a foto padrão só pode aparecer no topo, senão a troca acima mexeria em outra seção
    fora_do_topo = base_html.split('<figure class="hero-foto">')[1].split('</figure>', 1)[1]
    if 'assets/img/%s-' % FOTO_PADRAO in fora_do_topo:
        sys.exit('a foto do topo aparece também fora do topo; ajustar o gerador')
    for p in PAGINAS:
        h = gerar(base_html, p)
        open(p['slug'] + '.html', 'w', encoding='utf-8', newline='').write(h)
        print('ok', p['slug'] + '.html', len(h))
    hoje = date.today().isoformat()
    urls = [BASE] + [BASE + p['slug'] for p in PAGINAS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n' % (u, hoje) for u in urls)
    sm += '</urlset>\n'
    open('sitemap.xml', 'w', encoding='utf-8', newline='').write(sm)
    print('sitemap', len(urls), 'endereços')


if __name__ == '__main__':
    main()
