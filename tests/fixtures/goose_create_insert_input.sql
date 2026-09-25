-- +goose Up

DROP TABLE IF EXISTS esquema.tabela_exemplo;
CREATE TABLE esquema.tabela_exemplo (
    id_exemplo SMALLINT PRIMARY KEY,
    ds_exemplo VARCHAR( 100 ) NOT NULL
);

INSERT INTO esquema.tabela_exemplo (
    id_exemplo,
    ds_exemplo
) VALUES (
    1,
    'Descricao Exemplo'
);

-- +goose Down

DROP TABLE IF EXISTS esquema.tabela_exemplo;
