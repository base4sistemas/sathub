
Projeto SATHub
==============

.. image:: https://img.shields.io/badge/status-planning-red.svg
    :target: https://pypi.python.org/pypi/sathub/
    :alt: Development status

.. image:: https://img.shields.io/badge/python%20version-2.7-blue.svg
    :target: https://pypi.python.org/pypi/sathub/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/sathub.svg
    :target: https://pypi.python.org/pypi/sathub/
    :alt: License

.. image:: https://img.shields.io/pypi/v/sathub.svg
    :target: https://pypi.python.org/pypi/sathub/
    :alt: Latest version

.. image:: https://img.shields.io/badge/docs-latest-green.svg
    :target: http://sathub.readthedocs.org/
    :alt: Latest Documentation

-------

    This project is about `SAT-CF-e`_ which is a system for autorization and
    transmission of fiscal documents, developed by Finance Secretary of
    state of São Paulo, Brazil. This entire project, variables, methods and
    class names, as well as documentation, are written in brazilian
    portuguese.

    Refer to the `official web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).


Este projeto está relacionado à tecnologia `SAT-CF-e`_ para autorização e
transmissão de documentos CF-e (*Cupons Fiscais eletrônicos*).

SATHub é um projeto open-source baseado em `Flask`_ e `Flask-RESTful`_ para
prover uma API que possibilita que múltiplos pontos-de-venda (PDV) possam
compartilhar um único equipamento SAT. Por se tratar de uma API RESTful,
qualquer aplicação de ponto-de-venda pode invocar funções SAT, desde que seja
capaz de fazer requisições HTTP simples.

Também fornece um *front-end* web leve para tornar possível o acesso às funções
do equipamento SAT a partir de um navegador com suporte à HTML5.

.. image:: https://raw.github.com/base4sistemas/sathub/master/docs/_static/screenshots/20150919/composicao.png
    :align: center
    :alt: Screenshots do front-end SATHub.

Saiba mais acessando a `documentação do projeto SATHub`_ e a
`documentação do projeto SATCFe`_.

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. _`SATComum`: https://github.com/base4sistemas/satcomum>
.. _`SATCFe`: https://github.com/base4sistemas/satcfe
.. _`Python`: https://www.python.org/
.. _`Flask`: http://flask.pocoo.org/
.. _`Flask-RESTful`: https://flask-restful.readthedocs.org/

.. _`documentação do projeto SATHub`: http://sathub.readthedocs.org/
.. _`documentação do projeto SATCFe`: http://satcfe.readthedocs.org/

.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
