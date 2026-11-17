# OUZE Comunicação Visual: landing page

Página estática (HTML, CSS e JavaScript sem dependências) publicada na Vercel, projeto `ouze-lp`, em https://lp.ouzecv.com.br/.

- `index.html`: a página inteira. O formulário do fim da página é o mesmo que abre no botão "Entrar em contato".
- `assets/img/`: fotos em WebP (640 e 1280 px), logo, favicon e imagem de compartilhamento.
- `robots.txt` e `sitemap.xml`: para o domínio lp.ouzecv.com.br.
- Envio do formulário: `POST https://n8n.moirarte.com.br/webhook/ouze/lp` (JSON). Com `?teste=1` no endereço da página, o envio vai para `.../ouze/lp?teste=1` e o Google Tag Manager não carrega.
- Rastreamento: Google Tag Manager `GTM-PMR45V5S`. Eventos na camada de dados: `form_open`, `generate_lead`, `whatsapp_click`.
  Nunca usar `elemento.onclick = () => dataLayer.push(...)`: com o GTM carregado o push devolve `false` e o clique é cancelado. Usar `addEventListener` sem devolver valor.
- H1 conforme o anúncio: `utm_term` (ou `utm_campaign`) escolhe um texto de uma lista fechada no script (`H1_GRUPO`). O texto da URL nunca vai para a página.
- Celular (até 760 px): grupos de cards viram carrossel com deslize lateral (`data-carrossel`), com pontinhos e teclado.
- Agentes de IA: `llms.txt` na raiz (resumo da OUZE e as 7 páginas) e o formulário do rodapé registrado como ferramenta WebMCP `solicitar_orcamento` (atributos `toolname`, `tooldescription` e `toolparamdescription`). A cópia do modal perde `toolname` e `tooldescription`, para existir uma ferramenta só. Quando um agente envia, o `submit` devolve o resultado em texto com `respondWith`.

Publicar: copiar `index.html`, `assets/`, `robots.txt`, `sitemap.xml`, `vercel.json` e `.vercel/` para uma pasta SEM `.git` e rodar ali
`vercel deploy --prod --yes --scope klohferramantas-3005s-projects`. Rodando dentro do repositório, a Vercel lê o autor do commit
(que não é membro da conta da unidade) e a publicação fica BLOCKED.
