# -*- coding: utf-8 -*-
"""Renders the four legal pages from one shell so PT and EN can never drift."""
import io
import os

TODO = '<span class="todo">{}</span>'

SHELL = """<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} | Infinite World</title>
    <meta name="description" content="{desc}" />
    <link rel="alternate" hreflang="{other_lang}" href="{sibling}" />
    <link rel="icon" type="image/png" href="assets/favicon-256.png" />
    <link
      rel="preload"
      href="assets/fonts/montserrat-latin.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header id="nav">
      <div class="nav-inner">
        <a class="brand" href="index.html" aria-label="Infinite World">
          <img src="assets/simbolo-transparente-escuro-2048.png" alt="" />
          <span class="wm">INFINITE WORLD</span>
        </a>
        <nav class="nav-links">
          <a href="index.html">{home}</a>
          <a href="{other_doc}">{other_doc_label}</a>
        </nav>
        <div class="nav-right">
          <a class="lang" href="{sibling}" hreflang="{other_lang}"
            ><b>{this_lang_up}</b><span>/ {other_lang_up}</span></a
          >
        </div>
      </div>
    </header>

    <main class="legal">
      <div class="container narrow">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="legal-meta">{updated}</p>
        <p class="lead">{lead}</p>
{body}
      </div>
    </main>

    <footer id="footer">
      <div class="container footer-inner">
        <div class="foot-brand">
          <div class="brand-lockup">
            <img
              src="assets/simbolo-transparente-escuro-2048.png"
              alt=""
            /><span>INFINITE WORLD</span>
          </div>
          <p class="tagline">{tagline}</p>
        </div>
        <div class="foot-legal">
          <p>INFINITE WORLD MARKETING SERVICES VIA SOCIAL MEDIA CO. L.L.C.</p>
          <p>
            Office OFF307-374 &middot; Dubai Investment Park 1 (DIP 1) &middot;
            Dubai
          </p>
          <p>United Arab Emirates &middot; www.infiniteworld.group</p>
          <p class="foot-links">
            <a href="{privacy_href}">{privacy_label}</a> &middot;
            <a href="{notice_href}">{notice_label}</a>
          </p>
          <p class="copy">&copy; 2026 Infinite World &middot; {rights}</p>
        </div>
      </div>
    </footer>
  </body>
</html>
"""


def sec(n, title, *blocks):
    inner = "\n".join("          " + b for b in blocks)
    return (
        '        <section class="legal-sec">\n'
        '          <h2><span class="legal-n">' + n + "</span>" + title + "</h2>\n"
        + inner
        + "\n        </section>"
    )


def table(headers, rows):
    head = "".join("<th>" + h + "</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join("<td>" + c + "</td>" for c in r) + "</tr>" for r in rows
    )
    return (
        '<div class="table-wrap"><table class="legal-table">'
        "<thead><tr>" + head + "</tr></thead><tbody>" + body + "</tbody></table></div>"
    )


def ul(*items):
    return "<ul>" + "".join("<li>" + i + "</li>" for i in items) + "</ul>"


ADDRESS = (
    '<p class="addr">INFINITE WORLD MARKETING SERVICES VIA SOCIAL MEDIA CO. L.L.C.'
    "<br />Office OFF307-374, Dubai Investment Park 1 (DIP 1)"
    "<br />Dubai, United Arab Emirates</p>"
)

PAGES = {}

PAGES["privacidade.html"] = dict(
    lang="pt",
    sibling="privacy.html",
    this_lang_up="PT",
    other_lang="en",
    other_lang_up="EN",
    home="Início",
    other_doc="aviso-legal.html",
    other_doc_label="Aviso Legal",
    eyebrow="DOCUMENTO LEGAL",
    title="Aviso de Privacidade",
    h1="Aviso de Privacidade",
    desc="Que dados este sítio recolhe, com que fundamento, quem lhes acede e que direitos tem sobre eles.",
    updated="Última atualização: 9 de setembro de 2026",
    lead="Este aviso explica que dados este sítio recolhe, porquê, quem lhes acede e que direitos tem sobre eles. Está escrito para cumprir os artigos 13.º e 14.º do Regulamento Geral sobre a Proteção de Dados da União Europeia.",
    tagline="Construído à escala do infinito.",
    privacy_href="privacidade.html",
    privacy_label="Privacidade",
    notice_href="aviso-legal.html",
    notice_label="Aviso Legal",
    rights="Todos os direitos reservados.",
    body="\n".join(
        [
            sec(
                "01",
                "Quem é o responsável pelo tratamento",
                ADDRESS,
                "<p>Email: "
                + TODO.format("por confirmar: endereço de email oficial")
                + "</p>",
                "<p>Encarregado de proteção de dados: "
                + TODO.format(
                    "por confirmar: nome e contacto, ou declaração de que não foi designado"
                )
                + "</p>",
                "<p>Representante na União Europeia: "
                + TODO.format("por confirmar: nome, morada e contacto")
                + "</p>",
                '<p class="fine">O artigo 27.º do Regulamento obriga o responsável estabelecido fora da União a designar por escrito um representante na União quando oferece bens ou serviços a pessoas que aí se encontram, salvo se o tratamento for ocasional, não abranger categorias especiais de dados em larga escala e for improvável que implique risco para os direitos dos titulares.</p>',
            ),
            sec(
                "02",
                "Que dados são tratados",
                ul(
                    "<b>Registos técnicos de servidor.</b> Cada visita gera um registo com endereço IP, tipo de navegador e sistema operativo, data e hora e página pedida. Estes registos são criados e conservados pela empresa que aloja este sítio, não por nós.",
                    "<b>Preferência de idioma.</b> Quando escolhe português ou inglês, essa escolha é guardada no seu próprio equipamento, no armazenamento local do navegador, sob a chave <code>iw_lang</code>. Não é enviada para nós nem para terceiros e pode apagá-la nas definições do navegador.",
                    "<b>O que nos enviar por email.</b> O botão de contacto abre o seu programa de email. Recebemos apenas o que decidir escrever: tipicamente nome, endereço de email, empresa e o conteúdo da mensagem.",
                ),
                "<p>Este sítio não tem formulários, não usa ferramentas de analítica ou de medição de audiências, não faz publicidade, não constrói perfis de visitante e não partilha dados com intermediários de publicidade.</p>",
            ),
            sec(
                "03",
                "Cookies e armazenamento local",
                "<p>Este sítio não instala cookies. A única informação guardada no seu equipamento é a preferência de idioma descrita acima, estritamente necessária para lhe entregar o sítio no idioma que pediu, o que a dispensa de consentimento prévio nos termos do artigo 5.º, n.º 3 da Diretiva 2002/58/CE.</p>",
                "<p>Os tipos de letra são servidos a partir deste mesmo domínio. Ao carregar esta página, o seu navegador não faz qualquer pedido a servidores de terceiros.</p>",
            ),
            sec(
                "04",
                "Finalidades e base legal",
                table(
                    ["Finalidade", "Dados", "Base legal"],
                    [
                        [
                            "Manter o sítio disponível e seguro e detetar utilização abusiva",
                            "Registos técnicos de servidor",
                            "Interesse legítimo, artigo 6.º, n.º 1, alínea f)",
                        ],
                        [
                            "Apresentar o sítio no idioma escolhido",
                            "Preferência guardada no seu equipamento",
                            "Serviço expressamente pedido por si",
                        ],
                        [
                            "Responder a um pedido de contacto ou de demonstração",
                            "O que nos enviar por email",
                            "Diligências pré-contratuais, artigo 6.º, n.º 1, alínea b), e interesse legítimo, alínea f)",
                        ],
                    ],
                ),
                "<p>Não tratamos categorias especiais de dados na aceção do artigo 9.º e pedimos que não as inclua nas mensagens que nos enviar.</p>",
            ),
            sec(
                "05",
                "Quem tem acesso",
                ul(
                    "A empresa que aloja este sítio, "
                    + TODO.format(
                        "por confirmar: identificação do alojamento e respetiva morada"
                    )
                    + ", que gera e conserva os registos técnicos de servidor.",
                    "O fornecedor do nosso serviço de email, "
                    + TODO.format("por confirmar: identificação do fornecedor")
                    + ".",
                    "As sociedades do grupo Infinite World, apenas na medida do necessário para responder ao seu pedido.",
                ),
                "<p>Não há outros destinatários. Não vendemos dados pessoais.</p>",
            ),
            sec(
                "06",
                "Transferências para fora da União Europeia",
                "<p>Este sítio é operado a partir dos Emirados Árabes Unidos e alojado fora da União Europeia. Isso significa que os dados descritos no ponto 2 podem ser tratados em países terceiros.</p>",
                ul(
                    "Emirados Árabes Unidos, onde está estabelecido o responsável. Os Emirados Árabes Unidos não beneficiam de decisão de adequação da Comissão Europeia. Salvaguarda aplicável: "
                    + TODO.format(
                        "por confirmar com aconselhamento jurídico: cláusulas contratuais-tipo do artigo 46.º ou derrogação do artigo 49.º"
                    ),
                    "País onde o sítio está alojado: "
                    + TODO.format(
                        "por confirmar: país e mecanismo de transferência aplicável"
                    ),
                ),
                '<p class="fine">Pode pedir-nos cópia das salvaguardas aplicáveis pelos contactos indicados no ponto 1.</p>',
            ),
            sec(
                "07",
                "Durante quanto tempo",
                ul(
                    "Registos técnicos de servidor: "
                    + TODO.format("por confirmar: prazo praticado pelo alojamento")
                    + ". Não os consultamos, salvo em caso de incidente de segurança.",
                    "Preferência de idioma: permanece no seu equipamento até a apagar.",
                    "Mensagens de email: conservadas enquanto durar o contacto comercial e, depois disso, "
                    + TODO.format("por confirmar: prazo de conservação e de arquivo")
                    + ".",
                ),
            ),
            sec(
                "08",
                "Os seus direitos",
                "<p>Nos termos dos artigos 15.º a 22.º do Regulamento, tem direito de acesso aos seus dados, de retificação, de apagamento, de limitação do tratamento, de portabilidade e de oposição ao tratamento fundado em interesse legítimo. Quando o tratamento assentar no seu consentimento, pode retirá-lo a qualquer momento, sem afetar a licitude do que foi feito antes.</p>",
                "<p>Para exercer qualquer destes direitos escreva para "
                + TODO.format(
                    "por confirmar: endereço de email para o exercício de direitos"
                )
                + ". Respondemos no prazo de um mês a contar da receção do pedido.</p>",
                '<p>Tem também o direito de apresentar reclamação junto da autoridade de controlo do Estado-Membro onde reside, onde trabalha ou onde ocorreu a alegada infração. Em Portugal, a Comissão Nacional de Proteção de Dados, <a href="https://www.cnpd.pt" rel="noopener">www.cnpd.pt</a>.</p>',
            ),
            sec(
                "09",
                "Ligações para outros sítios",
                "<p>Este sítio pode conter ligações para sítios operados por terceiros. Não controlamos esses sítios e este aviso não se aplica a eles. Leia a política de privacidade de cada um.</p>",
            ),
            sec(
                "10",
                "Alterações a este aviso",
                "<p>Se este aviso mudar, publicamos a versão nova nesta página e atualizamos a data no topo. Recomendamos que a consulte antes de nos enviar dados.</p>",
            ),
        ]
    ),
)

PAGES["privacy.html"] = dict(
    lang="en",
    sibling="privacidade.html",
    this_lang_up="EN",
    other_lang="pt",
    other_lang_up="PT",
    home="Home",
    other_doc="legal-notice.html",
    other_doc_label="Legal Notice",
    eyebrow="LEGAL DOCUMENT",
    title="Privacy Notice",
    h1="Privacy Notice",
    desc="What data this site collects, on what basis, who has access to it and what rights you have over it.",
    updated="Last updated: 9 September 2026",
    lead="This notice explains what data this site collects, why, who has access to it and what rights you have over it. It is written to meet Articles 13 and 14 of the European Union General Data Protection Regulation.",
    tagline="Built to the scale of infinity.",
    privacy_href="privacy.html",
    privacy_label="Privacy",
    notice_href="legal-notice.html",
    notice_label="Legal Notice",
    rights="All rights reserved.",
    body="\n".join(
        [
            sec(
                "01",
                "Who the controller is",
                ADDRESS,
                "<p>Email: " + TODO.format("to confirm: official email address") + "</p>",
                "<p>Data protection officer: "
                + TODO.format(
                    "to confirm: name and contact, or a statement that none has been appointed"
                )
                + "</p>",
                "<p>Representative in the European Union: "
                + TODO.format("to confirm: name, address and contact")
                + "</p>",
                '<p class="fine">Article 27 of the Regulation requires a controller established outside the Union to designate a representative in the Union in writing when it offers goods or services to people located there, unless the processing is occasional, does not involve special categories of data on a large scale and is unlikely to result in a risk to the rights of data subjects.</p>',
            ),
            sec(
                "02",
                "What data is processed",
                ul(
                    "<b>Technical server logs.</b> Every visit generates a log with an IP address, browser and operating system type, date and time and the page requested. These logs are created and kept by the company hosting this site, not by us.",
                    "<b>Language preference.</b> When you choose Portuguese or English, that choice is stored on your own device, in the browser local storage, under the key <code>iw_lang</code>. It is never sent to us or to anyone else and you can clear it in your browser settings.",
                    "<b>Whatever you send us by email.</b> The contact button opens your own email client. We receive only what you choose to write: typically name, email address, company and the content of the message.",
                ),
                "<p>This site has no forms, uses no analytics or audience measurement tools, runs no advertising, builds no visitor profiles and shares no data with advertising intermediaries.</p>",
            ),
            sec(
                "03",
                "Cookies and local storage",
                "<p>This site sets no cookies. The only information stored on your device is the language preference described above, which is strictly necessary to deliver the site in the language you asked for and therefore requires no prior consent under Article 5(3) of Directive 2002/58/EC.</p>",
                "<p>Fonts are served from this same domain. Loading this page makes no request from your browser to any third party server.</p>",
            ),
            sec(
                "04",
                "Purposes and legal basis",
                table(
                    ["Purpose", "Data", "Legal basis"],
                    [
                        [
                            "Keeping the site available and secure and detecting abuse",
                            "Technical server logs",
                            "Legitimate interests, Article 6(1)(f)",
                        ],
                        [
                            "Showing the site in the language you chose",
                            "Preference stored on your device",
                            "A service you expressly requested",
                        ],
                        [
                            "Answering a contact or demo request",
                            "Whatever you send us by email",
                            "Pre-contractual steps, Article 6(1)(b), and legitimate interests, Article 6(1)(f)",
                        ],
                    ],
                ),
                "<p>We process no special categories of data within the meaning of Article 9 and we ask that you do not include any in the messages you send us.</p>",
            ),
            sec(
                "05",
                "Who has access",
                ul(
                    "The company hosting this site, "
                    + TODO.format("to confirm: host identity and address")
                    + ", which generates and keeps the technical server logs.",
                    "Our email service provider, "
                    + TODO.format("to confirm: provider identity")
                    + ".",
                    "Companies within the Infinite World group, only as far as needed to answer your request.",
                ),
                "<p>There are no other recipients. We do not sell personal data.</p>",
            ),
            sec(
                "06",
                "Transfers outside the European Union",
                "<p>This site is operated from the United Arab Emirates and hosted outside the European Union. This means the data described in section 2 may be processed in third countries.</p>",
                ul(
                    "United Arab Emirates, where the controller is established. The United Arab Emirates has no adequacy decision from the European Commission. Safeguard relied on: "
                    + TODO.format(
                        "to confirm with legal counsel: standard contractual clauses under Article 46 or a derogation under Article 49"
                    ),
                    "Country where the site is hosted: "
                    + TODO.format("to confirm: country and applicable transfer mechanism"),
                ),
                '<p class="fine">You may ask us for a copy of the applicable safeguards using the contacts in section 1.</p>',
            ),
            sec(
                "07",
                "How long data is kept",
                ul(
                    "Technical server logs: "
                    + TODO.format("to confirm: retention period applied by the host")
                    + ". We do not consult them except in the event of a security incident.",
                    "Language preference: stays on your device until you clear it.",
                    "Email messages: kept for the duration of the commercial contact and, after that, "
                    + TODO.format("to confirm: retention and archiving period")
                    + ".",
                ),
            ),
            sec(
                "08",
                "Your rights",
                "<p>Under Articles 15 to 22 of the Regulation you have the right to access your data, to have it corrected, to have it erased, to restrict processing, to data portability and to object to processing based on legitimate interests. Where processing is based on your consent, you may withdraw it at any time without affecting the lawfulness of processing carried out beforehand.</p>",
                "<p>To exercise any of these rights, write to "
                + TODO.format("to confirm: email address for rights requests")
                + ". We reply within one month of receiving the request.</p>",
                '<p>You also have the right to lodge a complaint with the supervisory authority of the Member State where you live, where you work or where the alleged infringement took place. In Portugal, that is the Comissão Nacional de Proteção de Dados, <a href="https://www.cnpd.pt" rel="noopener">www.cnpd.pt</a>.</p>',
            ),
            sec(
                "09",
                "Links to other sites",
                "<p>This site may link to sites operated by third parties. We do not control them and this notice does not apply to them. Read the privacy policy of each one.</p>",
            ),
            sec(
                "10",
                "Changes to this notice",
                "<p>If this notice changes, we publish the new version on this page and update the date at the top. We recommend reading it before sending us any data.</p>",
            ),
        ]
    ),
)

PAGES["aviso-legal.html"] = dict(
    lang="pt",
    sibling="legal-notice.html",
    this_lang_up="PT",
    other_lang="en",
    other_lang_up="EN",
    home="Início",
    other_doc="privacidade.html",
    other_doc_label="Privacidade",
    eyebrow="DOCUMENTO LEGAL",
    title="Aviso Legal",
    h1="Aviso Legal",
    desc="Identificação legal do responsável por este sítio, exigida pelo artigo 5.º, n.º 1 da Diretiva 2000/31/CE.",
    updated="Última atualização: 9 de setembro de 2026",
    lead="Informação de identificação de acesso permanente, exigida a qualquer prestador de serviços da sociedade da informação pelo artigo 5.º, n.º 1 da Diretiva 2000/31/CE, sobre comércio eletrónico.",
    tagline="Construído à escala do infinito.",
    privacy_href="privacidade.html",
    privacy_label="Privacidade",
    notice_href="aviso-legal.html",
    notice_label="Aviso Legal",
    rights="Todos os direitos reservados.",
    body="\n".join(
        [
            sec(
                "01",
                "Identidade",
                ADDRESS,
                "<p>Forma jurídica: Limited Liability Company (L.L.C.), constituída ao abrigo do direito dos Emirados Árabes Unidos.</p>",
                '<p class="fine">Hub europeu: Bruxelas, Bélgica. Base operacional europeia e centro de conformidade regulatória da companhia. '
                + TODO.format("por confirmar: morada completa e forma jurídica da entidade em Bruxelas")
                + "</p>",
            ),
            sec(
                "02",
                "Contacto",
                ul(
                    "Email: " + TODO.format("por confirmar: endereço de email oficial"),
                    "Telefone: " + TODO.format("por confirmar: número de telefone"),
                    'Sítio: <a href="index.html">www.infiniteworld.group</a>',
                ),
            ),
            sec(
                "03",
                "Registo e licenciamento",
                table(
                    ["Elemento", "Valor"],
                    [
                        ["Registo comercial", "2298842"],
                        ["Número da licença comercial", "1353734"],
                        [
                            "Autoridade emissora",
                            TODO.format("por confirmar: entidade licenciadora no Dubai"),
                        ],
                        [
                            "Número de registo fiscal (TRN)",
                            TODO.format("por confirmar, se aplicável"),
                        ],
                        [
                            "Número de identificação para efeitos de IVA na União Europeia",
                            TODO.format("por confirmar, se aplicável"),
                        ],
                    ],
                ),
            ),
            sec(
                "04",
                "Responsável pelo conteúdo",
                "<p>"
                + TODO.format(
                    "por confirmar: nome da pessoa responsável pelo conteúdo editorial"
                )
                + "</p>",
            ),
            sec(
                "05",
                "Propriedade intelectual",
                "<p>Os textos, imagens, capturas de ecrã, o símbolo do laço, a marca Infinite World e a estrutura deste sítio são propriedade da sociedade identificada no ponto 1 ou de sociedades do seu grupo, e estão protegidos por direito de autor e por direito de marcas. A reprodução, distribuição ou modificação, total ou parcial, sem autorização escrita prévia, não é permitida.</p>",
            ),
            sec(
                "06",
                "Ligações para sítios de terceiros",
                "<p>Quando este sítio remete para sítios operados por terceiros, essa remissão não implica controlo nem aprovação do respetivo conteúdo. A responsabilidade por esses conteúdos é de quem os publica.</p>",
            ),
            sec(
                "07",
                "Natureza do conteúdo",
                "<p>A informação publicada neste sítio tem finalidade institucional e informativa. Não constitui oferta contratual, proposta comercial vinculativa nem aconselhamento profissional. As condições de qualquer prestação de serviços são fixadas em contrato escrito.</p>",
            ),
            sec(
                "08",
                "Proteção de dados",
                '<p>O tratamento de dados pessoais relacionado com este sítio está descrito no <a href="privacidade.html">Aviso de Privacidade</a>.</p>',
            ),
        ]
    ),
)

PAGES["legal-notice.html"] = dict(
    lang="en",
    sibling="aviso-legal.html",
    this_lang_up="EN",
    other_lang="pt",
    other_lang_up="PT",
    home="Home",
    other_doc="privacy.html",
    other_doc_label="Privacy",
    eyebrow="LEGAL DOCUMENT",
    title="Legal Notice",
    h1="Legal Notice",
    desc="Legal identification of the party responsible for this site, required by Article 5(1) of Directive 2000/31/EC.",
    updated="Last updated: 9 September 2026",
    lead="Permanently accessible identification information, required of any information society service provider by Article 5(1) of Directive 2000/31/EC on electronic commerce.",
    tagline="Built to the scale of infinity.",
    privacy_href="privacy.html",
    privacy_label="Privacy",
    notice_href="legal-notice.html",
    notice_label="Legal Notice",
    rights="All rights reserved.",
    body="\n".join(
        [
            sec(
                "01",
                "Identity",
                ADDRESS,
                "<p>Legal form: Limited Liability Company (L.L.C.), incorporated under the law of the United Arab Emirates.</p>",
                "<p class=\"fine\">European hub: Brussels, Belgium. The European operating base and regulatory compliance centre of the company. "
                + TODO.format("to confirm: full address and legal form of the Brussels entity")
                + "</p>",
            ),
            sec(
                "02",
                "Contact",
                ul(
                    "Email: " + TODO.format("to confirm: official email address"),
                    "Telephone: " + TODO.format("to confirm: telephone number"),
                    'Website: <a href="index.html">www.infiniteworld.group</a>',
                ),
            ),
            sec(
                "03",
                "Registration and licensing",
                table(
                    ["Item", "Value"],
                    [
                        ["Commercial register", "2298842"],
                        ["Commercial licence number", "1353734"],
                        [
                            "Issuing authority",
                            TODO.format("to confirm: Dubai licensing authority"),
                        ],
                        [
                            "Tax registration number (TRN)",
                            TODO.format("to confirm, if applicable"),
                        ],
                        [
                            "European Union VAT identification number",
                            TODO.format("to confirm, if applicable"),
                        ],
                    ],
                ),
            ),
            sec(
                "04",
                "Responsible for content",
                "<p>"
                + TODO.format(
                    "to confirm: name of the person responsible for editorial content"
                )
                + "</p>",
            ),
            sec(
                "05",
                "Intellectual property",
                "<p>The text, images, screen captures, the loop symbol, the Infinite World trade mark and the structure of this site are the property of the company identified in section 1 or of companies within its group, and are protected by copyright and trade mark law. Reproduction, distribution or modification, in whole or in part, without prior written permission is not permitted.</p>",
            ),
            sec(
                "06",
                "Links to third party sites",
                "<p>Where this site links to sites operated by third parties, that link implies neither control over nor endorsement of their content. Responsibility for that content lies with whoever publishes it.</p>",
            ),
            sec(
                "07",
                "Nature of the content",
                "<p>The information published on this site is institutional and informative. It is not a contractual offer, a binding commercial proposal or professional advice. The terms of any provision of services are set out in a written contract.</p>",
            ),
            sec(
                "08",
                "Data protection",
                '<p>Processing of personal data in connection with this site is described in the <a href="privacy.html">Privacy Notice</a>.</p>',
            ),
        ]
    ),
)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for name, data in PAGES.items():
    html = SHELL.format(**data)
    with io.open(os.path.join(root, name), "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    print("wrote", name, len(html), "bytes")
