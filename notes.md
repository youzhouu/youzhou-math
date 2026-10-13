---
layout: default
title: Notes
permalink: /notes/
---

Reading and study notes in partial differential equations and analysis.

<nav class="notes-index" aria-label="Note categories">
  <ul>
    {% for category in site.note_categories %}
    <li><a href="#{{ category.slug | escape }}">{{ category.title | escape }}</a></li>
    {% endfor %}
  </ul>
</nav>

{% for category in site.note_categories %}
<section class="note-category" id="{{ category.slug | escape }}">
  <h2>{{ category.title | escape }}</h2>
  <p>{{ category.description | escape }}</p>
  {% assign category_notes = site.notes | where: "category", category.slug | sort: "order" %}
  {% if category_notes.size > 0 %}
  <ul class="note-list">
    {% for note in category_notes %}
    <li>
      <a href="{{ note.url | relative_url }}">{{ note.title | escape }}</a>{% if note.pdf %} {% include pdf-link.html path=note.pdf label="PDF" %}{% endif %}
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="empty-notes">No notes available yet.</p>
  {% endif %}
</section>
{% endfor %}
