{{- $c := partial "md-clean.html" . -}}
{{- if eq .Layout "about" -}}
# {{ .Params.name | default .Title }}

{{ with .Params.role }}{{ . }}

{{ end }}- URL: {{ .Permalink }}
{{ with site.Params.author.sameAs }}{{ range . }}- Профиль: {{ . }}
{{ end }}{{ end }}
{{ $c }}
{{ with .Params.experience }}
## Опыт
{{ range . }}
- **{{ .org }}{{ if ne .years "MBA" }} ({{ .years }}){{ end }}.** {{ .text }}
{{- end }}
{{ end }}
{{ with .Params.education }}
## Образование
{{ range . }}
- **{{ .org }}{{ if ne .years "MBA" }} ({{ .years }}){{ end }}.** {{ .text }}
{{- end }}
{{ end }}
{{- else -}}
# {{ .Title }}

{{ with .Description }}> {{ . }}

{{ end }}- URL: {{ .Permalink }}
- Дата: {{ .Date.Format "2006-01-02" }}
{{ with .Params.author }}- Автор: {{ . }}
{{ end }}{{ with .Params.linkedin }}- Оригинал: {{ . }}
{{ end }}{{ with .Params.tags }}- Теги: {{ delimit . ", " }}
{{ end }}
{{ with .Params.lead }}{{ . }}

{{ end }}{{ $c }}
{{- end }}
