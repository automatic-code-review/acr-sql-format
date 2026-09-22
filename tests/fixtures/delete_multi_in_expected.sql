DELETE FROM
    acervo.configuracao_pagina cp
WHERE
    cp.id_configuracao_pagina IN ( :IDS_CONFIGURACAO_PAGINA ) AND
    cp.id_tipo IN ( :IDS_TIPO ) AND
    cp.ativo = 1;
