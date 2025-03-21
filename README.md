# acr-sql-format

Arquivo config.json

```json
{
  "path_source": "/tmp/my-project",
  "path_output": "output.json",
  "message": "Verifique a identação do SQL no arquivo: ${FILE_PATH}<br>Identação correta é:<br><br>${FORMATTED}",
  "merge": {
    "changes": [
      {
        "new_path": "folder/file.sql",
        "deleted_file": false
      }
    ]
  }
}
```
