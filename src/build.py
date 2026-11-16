#!/usr/bin/env python3
"""Génère le site statique INGEPLUS dans ../site/ .
Modifier les contenus ici (DATA), puis relancer :  python3 build.py
"""
import os, json, html
from urllib.parse import quote

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://www.ingeplus.ma'
REMOTE_IMG = DOMAIN + '/images/'
PHONE, PHONE_LINK = '+212 528 226 988', '+212528226988'
EMAIL = 'contact@ingeplus.ma'
LINKEDIN = 'https://www.linkedin.com/company/ingeplus-maroc/about/'
CERT = DOMAIN + '/' + quote("CERTIFICAT D'AGREMENT INGEPLUS -17-09-2026.pdf")
e = html.escape

# ------------------------------------------------------------------ icons
ICONS = {
 'structure':'<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6M5 12h14"/>',
 'elec':'<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
 'fluid':'<path d="M12 2.7s-6 6.6-6 11a6 6 0 0 0 12 0c0-4.4-6-11-6-11z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
 'pm':'<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M7 14h4M7 17h8"/>',
 'vrd':'<path d="M4 21 9 3M20 21 15 3M12 6v2M12 11v2M12 16v2"/>',
 'fire':'<path d="M12 22c4 0 7-3 7-7 0-3-2-5.5-3.5-7-.5 2-1.5 3-3 3.5C13 8 12 5 9 2c0 4-4 6.5-4 13 0 4 3 7 7 7z"/>',
 'seal':'<circle cx="12" cy="9" r="6"/><path d="M8.5 13.5 7 22l5-3 5 3-1.5-8.5M9.5 9l1.8 1.8L15 7.5"/>',
 'target':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'handshake':'<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a3 3 0 0 1 4 0L21 7.5M3 13l6 6M3 7l4-4 4 4"/>',
 'coins':'<circle cx="8" cy="8" r="6"/><path d="M18.1 10.4A6 6 0 1 1 10.3 18M7 6h1v4M16.7 13.9l.7.7-2.8 2.8"/>',
 'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
 'linkedin':'<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/>',
 'pin':'<path d="M12 22s7-6.1 7-12a7 7 0 0 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'zoom':'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5M11 8v6M8 11h6"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'doc':'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
}
def ico(name, cls=''):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" {cls}>{ICONS[name]}</svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def img(file, alt, root, extra=''):
    """Image locale (images/) avec repli automatique sur ingeplus.ma."""
    return (f'<img src="{root}images/{quote(file)}" data-fb="{REMOTE_IMG}{quote(file)}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async" {extra}>')

# ------------------------------------------------------------------ data
SERVICES = [
 dict(slug='ingenierie-des-structures', icon='structure', short='Structures',
  title='Ingénierie des structures',
  tagline="Béton armé, charpente métallique, bois et structures mixtes.",
  summary="Béton armé, charpente métallique, bois ou systèmes mixtes : de la conception au dimensionnement, nous garantissons la stabilité et la conformité de vos ouvrages.",
  body=["L’ingénierie des structures constitue le cœur technique de la construction. Notre mission est de transformer la vision architecturale en une réalité solide, sûre et durable.",
        "Nous intervenons sur tous types de structures : béton armé, charpente métallique, bois ou systèmes mixtes. De la conception au dimensionnement, nos experts en génie civil s’engagent à garantir la stabilité et la conformité de vos bâtiments et ouvrages d'art, quel que soit leur degré de complexité."],
  missions=[('Conception structurelle','Choix du système porteur en étroite collaboration avec l’architecte.'),
            ('Notes de calcul','Descente de charges, dimensionnement et justification des éléments.'),
            ('Étude parasismique','Analyse et justification conformes au règlement RPS 2000.'),
            ('Plans d’exécution','Plans de coffrage et de ferraillage, détails d’assemblage.'),
            ('Fondations & soutènements','Choix et dimensionnement à partir de l’étude géotechnique.'),
            ('Suivi de chantier','Visa des plans, visites et contrôle de conformité.')],
  tags=['Béton armé','Charpente métallique','Bois','Structures mixtes','Ouvrages d’art']),
 dict(slug='etudes-electricite-cfo-cfa', icon='elec', short='Électricité CFO/CFA',
  title="Études d'électricité CFO/CFA",
  tagline="Courants forts et courants faibles.",
  summary="Conception électrique et planification stratégique des installations courants forts et courants faibles, optimisées pour l’efficacité.",
  body=["Nos ingénieurs et techniciens électriques possèdent une expertise avancée en matière de conception électrique et de planification stratégique. Ils savent anticiper et intégrer les contraintes techniques spécifiques de chaque projet.",
        "Grâce à leur savoir-faire, ils transforment des idées en plans concrets tout en optimisant la planification des installations électriques pour maximiser l’efficacité."],
  missions=[('Bilan de puissance','Évaluation des besoins et dimensionnement de l’alimentation.'),
            ('Courants forts (CFO)','Distribution, tableaux, éclairage, prises de force, groupes électrogènes.'),
            ('Courants faibles (CFA)','Réseaux VDI, contrôle d’accès, vidéosurveillance, détection.'),
            ('Postes de transformation','Conception des postes MT/BT en lien avec le distributeur.'),
            ('Éclairage','Études d’éclairement intérieur et extérieur.'),
            ('Dossiers DCE','Plans, CCTP, bordereaux et estimations.')],
  tags=['Courants forts','Courants faibles','Éclairage','MT/BT']),
 dict(slug='etudes-des-fluides', icon='fluid', short='Fluides CVC / Plomberie',
  title='Études des fluides',
  tagline="Chauffage, ventilation, climatisation, plomberie et ECS.",
  summary="Stratégies de conception en CVC et Plomberie/ECS, avec une maîtrise budgétaire rigoureuse dès les premières phases.",
  body=["Spécialistes en ingénierie des fluides, nous définissons les stratégies de conception en CVC (Chauffage, Ventilation, Climatisation) et Plomberie/ECS.",
        "Notre expertise en amont permet une maîtrise budgétaire rigoureuse, un conseil pertinent sur le choix des matériels et une sécurisation des phases de conception technique (PRO-DCE)."],
  missions=[('Bilans thermiques','Calcul des apports et déperditions, choix des systèmes.'),
            ('Climatisation & chauffage','Conception des installations et des réseaux de distribution.'),
            ('Ventilation','Renouvellement d’air, VMC et traitement d’air.'),
            ('Plomberie & ECS','Alimentation en eau, production d’eau chaude, évacuations.'),
            ('Thermique du bâtiment','Accompagnement à la conformité RTCM.'),
            ('Phases PRO-DCE','Plans, pièces écrites et estimation des lots techniques.')],
  tags=['CVC','Plomberie','ECS','Thermique','PRO-DCE']),
 dict(slug='gestion-de-projet', icon='pm', short='Gestion de projet',
  title='Gestion de projet',
  tagline="Pilotage, coordination et analyse financière.",
  summary="Pilotage de projet et analyse financière à toutes les étapes du cycle de vie, de la conception à la clôture.",
  body=["Nos experts assurent le pilotage de projet (délais, qualité, coûts, coordination) avec l'analyse financière (estimation des coûts, faisabilité, rentabilité) à toutes les étapes du cycle de vie.",
        "De la conception à la clôture, nous veillons à assurer le succès technique et économique de votre opération."],
  missions=[('Études de faisabilité','Analyse technique, financière et réglementaire du projet.'),
            ('Estimation des coûts','Budgets prévisionnels et suivi économique par lot.'),
            ('Planification','Plannings directeurs et d’exécution, suivi des jalons.'),
            ('Coordination (OPC)','Ordonnancement et coordination des intervenants.'),
            ('Contrôle qualité','Suivi des performances et conformité des ouvrages.'),
            ('Assistance à la réception','Levée des réserves et clôture de l’opération.')],
  tags=['Pilotage','OPC','Estimation','Faisabilité','Rentabilité']),
 dict(slug='ingenierie-vrd', icon='vrd', short='VRD',
  title='Ingénierie VRD',
  tagline="Voirie et Réseaux Divers.",
  summary="Diagnostics de faisabilité et suivi opérationnel pour des aménagements réalisés dans les règles de l'art.",
  body=["Chez INGEPLUS, nous plaçons l'expertise VRD et infrastructures au service de vos ambitions. Nos équipes s'engagent à transformer les contraintes de vos terrains en solutions optimisées.",
        "Grâce à nos diagnostics de faisabilité et notre suivi opérationnel, nous garantissons aux maîtres d’ouvrage des aménagements d’excellence, réalisés dans les règles de l'art."],
  missions=[('Diagnostic de faisabilité','Analyse topographique et des contraintes du terrain.'),
            ('Voirie','Tracés, profils en long et en travers, structures de chaussée.'),
            ('Assainissement','Réseaux eaux usées et eaux pluviales.'),
            ('Eau potable & incendie','Réseaux d’adduction et de défense incendie.'),
            ('Réseaux secs','Électricité, éclairage public, télécommunications.'),
            ('Lotissements','Conception et suivi des travaux d’aménagement.')],
  tags=['Voirie','Assainissement','AEP','Éclairage public','Lotissements']),
 dict(slug='securite-incendie', icon='fire', short='Sécurité incendie (ISI)',
  title='Ingénierie de la Sécurité Incendie (ISI)',
  tagline="Bureau d’études agréé par l’État en sécurité incendie.",
  summary="Conception, planification et déploiement de solutions de sécurité incendie à la pointe de l'innovation.",
  body=["En tant que bureau d’études agréé par l’État en sécurité incendie, nous mettons notre expertise et notre expérience à votre service pour garantir la sécurité de vos installations et de vos occupants.",
        "Chez INGEPLUS, nous sommes conscients de l’enjeu crucial que représente la sécurité incendie pour chaque projet. Notre équipe d’ingénieurs qualifiés est spécialisée dans la conception, la planification et le déploiement de solutions de sécurité à la pointe de l'innovation."],
  missions=[('Notice de sécurité','Analyse réglementaire et classement de l’établissement.'),
            ('Détection & alarme','Conception des systèmes de sécurité incendie.'),
            ('Désenfumage','Études de désenfumage naturel et mécanique.'),
            ('Extinction','RIA, colonnes sèches, sprinklers et moyens de secours.'),
            ('Évacuation','Dégagements, issues de secours et compartimentage.'),
            ('Accompagnement','Assistance auprès des autorités et commissions.')],
  tags=['Agréé État','Détection','Désenfumage','Extinction','Évacuation']),
]

PROJECTS = [
 dict(t='Bâtiment logistique', l='Casablanca', c='industriel', cat='Logistique', img='casa.png'),
 dict(t='Immeuble de bureaux R+5 avec sous-sol', l='Agadir', c='tertiaire', cat='Tertiaire', img='masiyen.png'),
 dict(t='Complexe résidentiel mixte', l='Dcheira El Jihadia', c='residentiel', cat='Résidentiel', img='jihadia.png'),
 dict(t='Immeuble de bureaux R+7 avec deux sous-sols', l='Agadir', c='tertiaire', cat='Tertiaire', img='rsept.png'),
 dict(t='Hôtel 5 étoiles', l='Marrakech', c='tertiaire', cat='Hôtellerie', img='projnaidi.png'),
 dict(t='Lotissements résidentiels', l='Biougra', c='residentiel', cat='Aménagement', img='biougra.png'),
 dict(t='Unités industrielles', l='Agadir & Ouled Teima', c='industriel', cat='Industriel', img='Unite_Indus_vf.png'),
 dict(t='Centre pluridisciplinaire', l='Casablanca', c='equipement', cat='Équipement public', img='centre_casa.png'),
 dict(t='Lycée qualifiant', l='Boujdour', c='equipement', cat='Enseignement', img='lycee_boujdour.png'),
]
FILTERS = [('all','Tous'),('tertiaire','Tertiaire & hôtellerie'),('residentiel','Résidentiel'),('industriel','Industriel'),('equipement','Équipements publics')]
CLIENT_LOGOS = ['moubina.png','strapex.png','maroc.png','onssa.png','NCB BICHA.jpg','sante.png','islam.png','takhtit.png','lognaidi.png','MEEMAR TAMLEEK.png','INRA.jpg','Men_2021.PNG']

VALUES = [('target','Rigueur','Professionnalisme et exigence technique.'),
          ('handshake','Engagement','Un suivi à chaque étape du projet.'),
          ('shield','Fiabilité','Des solutions techniques fiables et adaptées.'),
          ('coins','Maîtrise des coûts','Le budget suivi à chaque phase.')]

PROCESS = [('Faisabilité','Analyse du programme, du terrain et de la réglementation. Première estimation du coût.'),
           ('Études','APS, APD et PRO, avec une coordination entre tous les lots techniques.'),
           ('Consultation','Dossier de consultation des entreprises et analyse des offres.'),
           ('Suivi des travaux','Visites de chantier, contrôle de conformité et réception.')]

FAQ = [('Comment démarrer un projet avec INGEPLUS ?','Contactez-nous par téléphone, e-mail ou via le formulaire de contact pour planifier une première consultation. Nous analysons votre besoin et vous adressons une proposition adaptée.'),
       ('Quels services proposez-vous ?','Ingénierie des structures, études électriques CFO/CFA, études des fluides (CVC, plomberie, ECS), ingénierie VRD, sécurité incendie (ISI) et gestion de projet.'),
       ('INGEPLUS est-il un bureau d’études agréé ?','Oui. INGEPLUS est un bureau d’études agréé par l’État, y compris en ingénierie de la sécurité incendie. Le certificat d’agrément est consultable en ligne.'),
       ('Quels sont les délais d’une étude ?','Les délais dépendent de la nature et de l’envergure du projet. Ils sont définis avec vous dès la consultation initiale, puis suivis rigoureusement tout au long de la mission.'),
 ]

# ------------------------------------------------------------------ layout
NAV = [('index.html','Accueil','home'),('a-propos.html','Qui sommes-nous','about'),('expertises.html','Nos métiers','expertises'),
       ('projets.html','Références','projets'),('contact.html','Contact','contact')]

def head(title, desc, path, root, extra_ld=None):
    url = DOMAIN + '/' + (path if path != 'index.html' else '')
    ld = {"@context":"https://schema.org","@type":"ProfessionalService","name":"INGEPLUS",
          "description":"Bureau d'études pluridisciplinaire agréé par l'État au Maroc.",
          "url":DOMAIN,"logo":REMOTE_IMG+'logo.png',"telephone":PHONE_LINK,"email":EMAIL,
          "areaServed":"MA","sameAs":[LINKEDIN],
          "knowsAbout":[s['title'] for s in SERVICES]}
    lds = [ld] + ([extra_ld] if extra_ld else [])
    return f'''<!DOCTYPE html>
<html lang="fr" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b1b2b">
<meta property="og:type" content="website">
<meta property="og:site_name" content="INGEPLUS">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{REMOTE_IMG}rsept.png">
<meta property="og:locale" content="fr_MA">
<link rel="icon" href="{root}images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
'''

def header(active, root):
    tb = f'''<div class="topbar"><div class="wrap">
  <div class="tb-left">
    <a href="tel:{PHONE_LINK}">{ico('phone')}<span>{PHONE}</span></a>
    <a href="mailto:{EMAIL}">{ico('mail')}<span>{EMAIL}</span></a>
  </div>
</div></div>'''
    items = []
    for href, label, key in NAV:
        cls = ' class="active"' if key == active else ''
        if key == 'expertises':
            sub = ''.join(f'<li><a href="{root}expertises/{s["slug"]}.html"><span class="di">{ico(s["icon"])}</span>{e(s["title"])}</a></li>' for s in SERVICES)
            items.append(f'<li class="has-sub"><a href="{root}{href}"{cls} aria-haspopup="true">{label}<svg class="caret" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></a><ul class="dropdown">{sub}<li><a href="{root}{href}" style="color:var(--accent)">Tous nos métiers</a></li></ul></li>')
        else:
            items.append(f'<li><a href="{root}{href}"{cls}>{label}</a></li>')
    items.append(f'<li class="mobile-cta"><a href="{root}contact.html" class="btn btn-primary">Nous contacter</a></li>')
    return tb + f'''
<header class="site-header"><div class="wrap nav">
  <a href="{root}index.html" class="brand" aria-label="INGEPLUS – accueil">
    <img src="{root}images/logo.png" data-fb="{REMOTE_IMG}logo.png" alt="Logo INGEPLUS" width="48" height="48">
    <span class="wordmark">INGE<b>PLUS</b><small>Bureau d'études</small></span>
  </a>
  <nav aria-label="Navigation principale"><ul class="menu">{''.join(items)}</ul></nav>
  <a href="{root}contact.html" class="btn btn-primary">Nous contacter</a>
  <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false"><svg width="28" height="28" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div></header>
<main id="main">
'''

def footer(root, lightbox=False):
    svc = ''.join(f'<li><a href="{root}expertises/{s["slug"]}.html">{e(s["short"])}</a></li>' for s in SERVICES)
    lb = f'''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Visionneuse de projets">
  <button class="lb-btn lb-close" aria-label="Fermer"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  <button class="lb-btn lb-prev" aria-label="Précédent"><svg viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg></button>
  <button class="lb-btn lb-next" aria-label="Suivant"><svg viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg></button>
  <figure><img src="" alt=""><figcaption><div><small class="lb-cat"></small><strong class="lb-title"></strong></div><span class="lb-loc"></span></figcaption></figure>
</div>''' if lightbox else ''
    return f'''</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a href="{root}index.html" class="brand"><img src="{root}images/logo.png" data-fb="{REMOTE_IMG}logo.png" alt="" width="44" height="44"><span class="wordmark">INGE<b>PLUS</b></span></a>
        <p>Bureau d'études techniques pluridisciplinaire, agréé par l'État.</p>
        <div class="socials">
          <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{ico('linkedin')}</a>
          <a href="mailto:{EMAIL}" aria-label="E-mail">{ico('mail')}</a>
          <a href="tel:{PHONE_LINK}" aria-label="Téléphone">{ico('phone')}</a>
        </div>
      </div>
      <div><h3>Navigation</h3><ul>{''.join(f'<li><a href="{root}{h}">{l}</a></li>' for h,l,_ in NAV)}<li><a href="{CERT}" target="_blank" rel="noopener">Certificat d'agrément</a></li></ul></div>
      <div><h3>Nos métiers</h3><ul>{svc}</ul></div>
      <div><h3>Contact</h3><ul>
        <li><a href="tel:{PHONE_LINK}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">INGEPLUS sur LinkedIn</a></li>
      </ul><a href="{root}contact.html" class="btn btn-primary" style="margin-top:1.4rem">Nous contacter</a></div>
    </div>
    <div class="copy"><span>© <span id="year">2026</span> INGEPLUS. Tous droits réservés.</span><span><a href="{root}mentions-legales.html">Mentions légales</a></span></div>
  </div>
</footer>
<a href="#main" class="to-top" aria-label="Haut de page"><svg viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></a>
{lb}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
'''

def page_hero(title, sub, crumbs, root, bg=None):
    cr = f'<a href="{root}index.html">Accueil</a>'
    for label, href in crumbs:
        cr += ' <span aria-hidden="true">/</span> ' + (f'<a href="{href}">{e(label)}</a>' if href else f'<span aria-current="page">{e(label)}</span>')
    media = f'<div class="ph-media">{img(bg, "", root, "aria-hidden=\"true\"")}</div>' if bg else ''
    return f'''<section class="page-hero">{media}<div class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane">{cr}</nav>
  <h1>{title}</h1><p>{sub}</p>
</div></section>'''

def svc_cards(root, n=None):
    out = []
    for i, s in enumerate(SERVICES[:n] if n else SERVICES, 1):
        out.append(f'''<article class="svc"><span class="num">0{i}</span>
  <div class="ico">{ico(s['icon'])}</div><h3>{e(s['title'])}</h3><p>{e(s['summary'])}</p>
  <a class="link-arrow" href="{root}expertises/{s['slug']}.html">En savoir plus<span class="sr-only"> sur {e(s['title'])}</span></a></article>''')
    return '<div class="svc-grid">' + ''.join(out) + '</div>'

def proj_cards(root, items):
    out = []
    for p in items:
        out.append(f'''<button class="proj" data-c="{p['c']}" data-cat="{e(p['cat'])}" data-title="{e(p['t'])}" data-loc="{e(p['l'])}" aria-label="Voir le projet : {e(p['t'])}, {e(p['l'])}">
  {img(p['img'], p['t'] + ' – ' + p['l'], root)}
  <span class="zoom">{ico('zoom')}</span>
  <span class="cap"><small>{e(p['cat'])}</small><h3>{e(p['t'])}</h3><span class="loc">{ico('pin')}{e(p['l'])}</span></span>
</button>''')
    return '<div class="proj-grid">' + ''.join(out) + '</div>'

def clients_band(root):
    logos = ''.join(img(f, 'Référence client INGEPLUS', root) for f in CLIENT_LOGOS)
    return f'''<section class="clients" aria-labelledby="cl-t"><div class="wrap"><h2 id="cl-t">Ils nous font confiance</h2>
<div class="marquee"><div class="track">{logos}</div></div></div></section>'''

def approval_band(root):
    return f'''<div class="approval">
  <div class="seal">{ico('seal')}</div>
  <div><h3>Agrément de l’État</h3><p>INGEPLUS est titulaire de l’agrément de l’État pour les études techniques et l’ingénierie de la sécurité incendie.</p></div>
  <a href="{CERT}" target="_blank" rel="noopener" class="btn btn-line">Voir le certificat (PDF)</a>
</div>'''

def process_section(dark=False):
    steps = ''.join(f'<div class="step"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in PROCESS)
    return f'''<section class="{'bg-ink on-dark' if dark else 'bg-paper'}"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><h2>Notre démarche</h2><span class="title-bar"></span></div>
  <div class="process-grid">{steps}</div></div></section>'''

def cta_band(root, title='Vous avez un projet ?', sub='Contactez-nous pour en discuter avec nos ingénieurs.'):
    return f'''<section class="cta-band"><div class="wrap">
  <div><h2>{title}</h2><p>{sub}</p></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a href="tel:{PHONE_LINK}" class="btn btn-line">{PHONE}</a><a href="{root}contact.html" class="btn btn-dark">Nous contacter</a></div>
</div></section>'''

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)

# ------------------------------------------------------------------ pages
def home():
    r = ''
    body = f'''
<section class="hero">
  <div class="hero-media">{img('rsept.png','Immeuble de bureaux R+7 à Agadir', r, 'fetchpriority="high" loading="eager"')}</div>
  <div class="wrap"><div class="hero-content">
    <span class="eyebrow">Bureau d’études agréé par l’État</span>
    <h1>Bienvenue chez INGEPLUS</h1>
    <p>Bureau d’études techniques pluridisciplinaire : structures, électricité, fluides, VRD, sécurité incendie et gestion de projet.</p>
    <div class="hero-ctas"><a href="projets.html" class="btn btn-primary">Nos références</a><a href="contact.html" class="btn btn-ghost">Nous contacter</a></div>
  </div></div>
</section>

<section><div class="wrap split">
  <div>
    <span class="eyebrow">Qui sommes-nous</span>
    <h2>Votre partenaire de confiance en ingénierie</h2>
    <p>INGEPLUS est un bureau d’études pluridisciplinaire agréé par l’État. Nous intervenons en ingénierie des structures, des fluides, de l’électricité, de la thermique du bâtiment, des VRD et de la sécurité incendie.</p>
    <p>Nos missions couvrent les projets résidentiels, tertiaires, industriels et d’infrastructures, depuis la conception jusqu’au suivi des travaux et à la réception, dans le respect du triptyque coût, délai, qualité.</p>
    <a href="a-propos.html" class="btn btn-dark" style="margin-top:24px">En savoir plus</a>
  </div>
  <div class="split-media"><div class="main">{img('centre_casa.png','Centre pluridisciplinaire à Casablanca', r)}</div></div>
</div></section>

<section class="bg-paper"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><h2>Nos métiers</h2><span class="title-bar"></span></div>
  {svc_cards(r)}
</div></section>

<section><div class="wrap">
  <div class="sec-head"><h2>Nos références</h2><a href="projets.html" class="btn btn-line">Toutes les références</a></div>
  {proj_cards(r, PROJECTS[:6])}
</div></section>

<section style="padding-top:0"><div class="wrap">{approval_band(r)}</div></section>
{clients_band(r)}
{cta_band(r)}
'''
    write('index.html', head("INGEPLUS | Bureau d'études pluridisciplinaire agréé au Maroc",
        "INGEPLUS, bureau d'études agréé par l'État : ingénierie des structures, électricité CFO/CFA, fluides CVC, VRD, sécurité incendie et gestion de projet au Maroc.",
        'index.html', r) + header('home', r) + body + footer(r, lightbox=True))

def expertises():
    r = ''
    body = page_hero('Nos métiers', 'Notre expertise en ingénierie.',
                     [('Nos métiers', None)], r, 'masiyen.png') + f'''
<section class="bg-paper"><div class="wrap">{svc_cards(r)}</div></section>
{process_section(dark=True)}
<section><div class="wrap">{approval_band(r)}</div></section>
{cta_band(r)}'''
    write('expertises.html', head('Nos expertises | INGEPLUS', "Structures, électricité CFO/CFA, fluides, gestion de projet, VRD et sécurité incendie : découvrez les expertises d'INGEPLUS.", 'expertises.html', r)
          + header('expertises', r) + body + footer(r))

def service_page(i, s):
    r = '../'
    missions = ''.join(f'<div class="mission"><div><b>{e(t)}</b><span>{e(d)}</span></div></div>' for t, d in s['missions'])
    tags = ''.join(f'<span>{e(t)}</span>' for t in s['tags'])
    nav = ''.join(f'<a href="{x["slug"]}.html"{" class=\"active\" aria-current=\"page\"" if x is s else ""}>{e(x["short"])}</a>' for x in SERVICES)
    refs = [PROJECTS[(i * 2 + k) % len(PROJECTS)] for k in range(3)]
    body = page_hero(e(s['title']), e(s['tagline']), [('Nos métiers', '../expertises.html'), (s['short'], None)], r, refs[0]['img']) + f'''
<section><div class="wrap detail">
  <div class="prose">
    <h2>Présentation</h2>
    {''.join(f'<p>{e(p)}</p>' for p in s['body'])}
    <div class="phases">{tags}</div>
    <h2>Nos prestations</h2>
    <div class="missions">{missions}</div>
    <h2>Phases d’intervention</h2>
    <p>Mission complète ou partielle, selon le besoin du maître d’ouvrage.</p>
    <div class="phases"><span>APS</span><span>APD</span><span>PRO</span><span>DCE</span><span>Suivi des travaux</span><span>Réception</span></div>
  </div>
  <aside class="aside">
    <div class="aside-box"><h3>Nos métiers</h3><nav class="aside-nav">{nav}</nav></div>
    <div class="aside-cta"><h3>Une demande ?</h3><p>Appelez-nous ou envoyez-nous votre dossier.</p>
      <a class="tel" href="tel:{PHONE_LINK}">{PHONE}</a>
      <a href="../contact.html?expertise={quote(s['title'])}" class="btn btn-primary" style="width:100%;justify-content:center">Nous contacter</a></div>
    <div class="aside-box"><h3>Agrément</h3><p style="font-size:14px;color:var(--grey);margin-bottom:10px">INGEPLUS est agréé par l’État.</p><a class="link-arrow" href="{CERT}" target="_blank" rel="noopener">Voir le certificat</a></div>
  </aside>
</div></section>
<section class="bg-paper"><div class="wrap">
  <div class="sec-head"><div><h2>Références</h2></div><a href="../projets.html" class="btn btn-line">Toutes les références</a></div>
  {proj_cards(r, refs)}
</div></section>
{cta_band(r)}'''
    ld = {"@context":"https://schema.org","@type":"Service","name":s['title'],"description":s['summary'],
          "provider":{"@type":"Organization","name":"INGEPLUS","url":DOMAIN},"areaServed":"MA"}
    write(f'expertises/{s["slug"]}.html', head(f'{s["title"]} | INGEPLUS', s['summary'], f'expertises/{s["slug"]}.html', r, ld)
          + header('expertises', r) + body + footer(r, lightbox=True))

def projets():
    r = ''
    filters = ''.join(f'<button data-f="{k}" class="{"on" if k=="all" else ""}" aria-pressed="{"true" if k=="all" else "false"}">{l}</button>' for k, l in FILTERS)
    body = page_hero('Nos références', 'Quelques projets réalisés par INGEPLUS.',
                     [('Références', None)], r, 'projnaidi.png') + f'''
<section><div class="wrap">
  <div class="sec-head"><div class="filters" aria-label="Filtrer les projets">{filters}</div></div>
  {proj_cards(r, PROJECTS)}
</div></section>
{clients_band(r)}
{cta_band(r)}'''
    write('projets.html', head('Projets et références | INGEPLUS', "Découvrez les références d'INGEPLUS : immeubles de bureaux, hôtel 5 étoiles, unités industrielles, lotissements et équipements publics au Maroc.", 'projets.html', r)
          + header('projets', r) + body + footer(r, lightbox=True))

def about():
    r = ''
    vals = ''.join(f'<div class="value"><div class="ico">{ico(i)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in VALUES)
    faq = ''.join(f'<details{" open" if k==0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for k, (q, a) in enumerate(FAQ))
    body = page_hero('Qui sommes-nous', 'Bureau d’études techniques pluridisciplinaire agréé par l’État.',
                     [('Qui sommes-nous', None)], r, 'jihadia.png') + f'''
<section><div class="wrap split">
  <div >
    <h2>INGEPLUS</h2>
    <p class="lead">INGEPLUS est un bureau d’études pluridisciplinaire agréé par l’État marocain, spécialisé en ingénierie des structures, des fluides, de l’électricité, de la thermique du bâtiment, des VRD et de la sécurité incendie.</p>
    <p class="lead" style="margin-top:12px">Nous intervenons sur des projets résidentiels, tertiaires, industriels et d’infrastructures, de la conception jusqu’au suivi d’exécution et à la réception des ouvrages. Notre engagement : l’équilibre coût, délai, qualité sur chaque projet.</p>
  </div>
  <div class="split-media">
    <div class="main">{img('Unite_Indus_vf.png','Unités industrielles à Agadir et Ouled Teima', r)}</div>
    <div class="float"><b>Agréé État</b><span>Études techniques & sécurité incendie</span></div>
  </div>
</div></section>
<section class="bg-paper"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><h2>Nos valeurs</h2><span class="title-bar"></span></div>
  <div class="values">{vals}</div>
</div></section>
{process_section(dark=True)}
<section><div class="wrap">{approval_band(r)}</div></section>
<section class="bg-paper" id="faq"><div class="wrap faq-grid">
  <div ><h2>Questions fréquentes</h2><span class="title-bar"></span></div>
  <div >{faq}</div>
</div></section>
{clients_band(r)}
{cta_band(r)}'''
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ]}
    write('a-propos.html', head('À propos | INGEPLUS, bureau d’études agréé', "INGEPLUS, bureau d'études pluridisciplinaire agréé par l'État marocain : nos valeurs, notre méthodologie et notre agrément.", 'a-propos.html', r, faq_ld)
          + header('about', r) + body + footer(r))

def contact():
    r = ''
    opts = ''.join(f'<option>{e(s["title"])}</option>' for s in SERVICES) + '<option>Mission pluridisciplinaire</option><option>Autre demande</option>'
    body = page_hero('Contact', 'Pour toute demande d’information ou de devis.',
                     [('Contact', None)], r, 'casa.png') + f'''
<section><div class="wrap contact-grid">
  <div>
    <h2>Coordonnées</h2><span class="title-bar"></span>
    <div class="cinfo">
      <a href="tel:{PHONE_LINK}"><span class="ci-ico">{ico('phone')}</span><div><small>Téléphone</small><strong>{PHONE}</strong></div></a>
      <a href="mailto:{EMAIL}"><span class="ci-ico">{ico('mail')}</span><div><small>E-mail</small><strong>{EMAIL}</strong></div></a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener"><span class="ci-ico">{ico('linkedin')}</span><div><small>LinkedIn</small><strong>INGEPLUS Maroc</strong></div></a>
      <a href="{CERT}" target="_blank" rel="noopener"><span class="ci-ico">{ico('doc')}</span><div><small>Agrément</small><strong>Certificat d’agrément (PDF)</strong></div></a>
    </div>
  </div>
  <div class="form-card">
    <h2>Formulaire de contact</h2><p>Les champs marqués * sont obligatoires.</p>
    <form id="contact-form" action="contact.php" method="post" novalidate>
      <div class="row">
        <label>Nom complet *<input name="nom" required autocomplete="name" placeholder="Votre nom"></label>
        <label>Société / organisme<input name="societe" autocomplete="organization" placeholder="Optionnel"></label>
      </div>
      <div class="row">
        <label>E-mail *<input type="email" name="email" required autocomplete="email" placeholder="vous@exemple.com"></label>
        <label>Téléphone<input type="tel" name="tel" autocomplete="tel" placeholder="+212 6 …"></label>
      </div>
      <div class="row">
        <label>Domaine concerné<select name="service">{opts}</select></label>
        <label>Ville du projet<input name="ville" placeholder="Ex. : Agadir"></label>
      </div>
      <label>Votre message *<textarea name="message" required placeholder="Décrivez votre projet : nature, surface, phase d’étude, échéance…"></textarea></label>
      <label class="hp" aria-hidden="true">Ne pas remplir<input name="website" tabindex="-1" autocomplete="off"></label>
      <label class="consent"><input type="checkbox" name="consent" required> J’accepte que mes données soient utilisées par INGEPLUS pour répondre à ma demande.</label>
      <div class="form-status" role="status" aria-live="polite"></div>
      <button class="btn btn-primary" type="submit" style="justify-content:center">Envoyer ma demande</button>
    </form>
  </div>
</div></section>'''
    write('contact.html', head('Contact et demande de devis | INGEPLUS', "Contactez INGEPLUS pour vos études techniques : structures, électricité, fluides, VRD, sécurité incendie. Tél. +212 528 226 988.", 'contact.html', r)
          + header('contact', r) + body + footer(r))

def legal():
    r = ''
    body = page_hero('Mentions légales', 'Informations légales relatives au site ingeplus.ma.', [('Mentions légales', None)], r) + f'''
<section><div class="wrap prose" style="max-width:820px">
  <h2>Éditeur du site</h2>
  <p>INGEPLUS, bureau d’études pluridisciplinaire agréé par l’État.<br>Téléphone : {PHONE}<br>E-mail : {EMAIL}<br>
  <!-- À COMPLÉTER : forme juridique, adresse du siège, RC, ICE, IF, directeur de la publication --></p>
  <h2>Hébergement</h2>
  <p><!-- À COMPLÉTER : nom et adresse de l’hébergeur -->Informations sur l’hébergeur disponibles sur demande.</p>
  <h2>Propriété intellectuelle</h2>
  <p>L’ensemble des contenus de ce site (textes, images, logos) est la propriété d’INGEPLUS ou de ses partenaires. Toute reproduction sans autorisation préalable est interdite.</p>
  <h2>Données personnelles</h2>
  <p>Les informations transmises via le formulaire de contact sont utilisées uniquement pour répondre à votre demande et ne sont pas cédées à des tiers, conformément à la loi n° 09-08 relative à la protection des personnes physiques à l’égard du traitement des données à caractère personnel. Pour toute demande d’accès, de rectification ou de suppression, écrivez à {EMAIL}.</p>
</div></section>'''
    write('mentions-legales.html', head('Mentions légales | INGEPLUS', 'Mentions légales du site INGEPLUS.', 'mentions-legales.html', r) + header(None, r) + body + footer(r))

def notfound():
    r = '/'
    body = f'''<section class="notfound"><div><b>404</b><h1 style="font-size:2rem;margin:1rem 0">Page introuvable</h1>
<p class="lead" style="margin:0 auto 2rem">La page que vous recherchez n’existe pas ou a été déplacée.</p>
<a href="/index.html" class="btn btn-primary">Retour à l’accueil</a></div></section>'''
    write('404.html', head('Page introuvable | INGEPLUS', 'Page introuvable.', '404.html', r) + header(None, r) + body + footer(r))

def seo_files():
    pages = ['', 'expertises.html', 'projets.html', 'a-propos.html', 'contact.html', 'mentions-legales.html'] + [f'expertises/{s["slug"]}.html' for s in SERVICES]
    urls = ''.join(f'<url><loc>{DOMAIN}/{p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="" else "0.8"}</priority></url>\n' for p in pages)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')

if __name__ == '__main__':
    home(); expertises(); projets(); about(); contact(); legal(); notfound(); seo_files()
    for i, s in enumerate(SERVICES): service_page(i, s)
    print('Site généré dans', os.path.abspath(OUT))
