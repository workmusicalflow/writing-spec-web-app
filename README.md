Réalisation d'un système d'agents AI "Evaluator-Optimizer Workflow" basé sur Anthropic et Pydantic AI.

## Liens utiles au besoin pour comprendre Pydantic AI :

https://ai.pydantic.dev/
https://ai.pydantic.dev/multi-agent-applications
https://ai.pydantic.dev/logfire
https://ai.pydantic.dev/testing-evals
https://ai.pydantic.dev/message-history
https://ai.pydantic.dev/results
https://ai.pydantic.dev/tools
https://ai.pydantic.dev/dependencies
https://ai.pydantic.dev/models
https://ai.pydantic.dev/agents

## Liens utiles au besoin pour Anthropic :

https://www.anthropic.com/research/building-effective-agents
https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/evaluator_optimizer.ipynb
https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/util.py

## Détails et Objectif de notre application Web

Nous construisons une application Gradio basée sur des agents AI spécialisés dans l'écriture de cahier des charges pour la réalisation d'application web.

Pour améliorer le workflow nous devons utiliser l'entrée utilisateur comme context et le rendre disponible à l'agent optimiseur via une dépendance ou des dépendances.

## Une entrée utilIsateur peut ressembler à ce type de prompt long :

**Contexte Général**
Projet de réalisation de site web destinée à la promotion d’évènement professionnel (Salon, forum international). Le site web à construire est destinée à l’évènement Africa QSHE Forum.

**Détails**
Le site est décrit comme suit dans le sens de la lecture et au scroll vers le bas:
Menu : Logo de l’évènement | Programme | Intervenants | Devenir exposant | Partenaires | Badge de participation | Editions précédentes
Bannière composée de textes dynamiques et images dynamique. Dans la div ou section de la bannière prévoir une zone d’information non dynamique pour la Date et le Lieu de l’évènement puis le bouton “Devenir Exposant”.
Courte présentation engageante et professionnelle de l’évènement “Africa QSHE Forum”, dans cette section nous devrons prévoir un bouton “Générer mon badge de visite”.
Les Intervenants; un échantillon des intervenants. Cet échantillon devra contenir 4 intervenants; cet échantillons devra s’actualiser à chaque rechargement de la page puis à une heure d’intervalle. Nous aurons un bouton “Découvrir la liste complète”.
Les partenaires; nous aurons à afficher tous les logos des partenaires. Nous aurons aussi un bouton “Devenir Partenaire (Sponsor)”.
Plan Map du lieu ou se tiendra l’évènement. Et un rappel de la date.
Le Footer contenant le logo de l’organisateur et ses contacts et liens sociaux.
La page des intervenants est une page qui contiendra des cartes présentant la photo, le nom, l’entreprise et le poste de chaque intervenant.
La page programme est une page qui contiendra un tableau contenant les jours (03), les tranches horaires et les activités par tranche horaire.
La page Édition précédente est une page qui contiendra une galerie photo des l’édition précédente et une Galerie vidéo des interventions (panels, cérémonie de lancement, visite de stands…)

## **Stack frontend**

- **HTML** : Structure de base.
- **Tailwind CSS** : Pour un design responsive et moderne.
- **Alpine.js** : Pour l'interactivité (gestion des états, événements, etc.).
- **Vanilla JS** : Pour les fonctionnalités spécifiques non couvertes par Alpine.js.

### **Backend**

- **Langage** : PHP (POO).
- **Architecture** : MVC (Modèle-Vue-Contrôleur) en utilisant “twig” pour le templating.
- **Bonnes pratiques** :
  - **TDD (Test-Driven Development)** : Écrire les tests avant le code.
  - **SOLID** : Principes de conception pour un code modulaire et maintenable.
  - **Clean Code** : Une intention par ligne de code, nommage clair, fonctions courtes.
  - **Code testable** : Isoler les dépendances, utiliser l'injection de dépendances.
- **Outils recommandés** :
  - **PHPUnit** : Pour les tests unitaires et fonctionnels.
  - **Composer** : Pour la gestion des dépendances.
  - **PDO** : Pour l'accès à la base de données SQLite.
