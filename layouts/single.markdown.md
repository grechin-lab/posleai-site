# {{ .Title }}

{{ with .Description }}> {{ . }}

{{ end }}- URL: {{ .Permalink }}
- Дата: {{ .Date.Format "2006-01-02" }}
{{ with .Params.author }}- Автор: {{ . }}
{{ end }}{{ with .Params.tags }}- Теги: {{ delimit . ", " }}
{{ end }}
{{ .RawContent }}
