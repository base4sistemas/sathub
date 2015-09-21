..
    SATHub documentation master file
    Created by sphinx-quickstart on Sun Sep 20 19:31:30 2015.

Bem-vindo ao Projeto SATHub
===========================

    This project is about `SAT-CF-e`_ which is a system for autorization and
    transmission of fiscal documents, developed by Finance Secretary of
    state of São Paulo, Brazil. This entire project, variables, methods and
    class names, as well as documentation, are written in brazilian
    portuguese.

    Refer to the `official web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).


.. note::

    **This documentation is a work in progress**


.. note::

    **Esta documentação é um trabalho em andamento**


Este projeto está relacionado à tecnologia `SAT-CF-e`_ para autorização e
transmissão de documentos CF-e (*Cupons Fiscais eletrônicos*).

SATHub é um projeto open-source baseado em `Flask`_ e `Flask-RESTful`_ para
prover uma API que possibilita que múltiplos pontos-de-venda (PDV) possam
compartilhar um único equipamento SAT. Por se tratar de uma API RESTful,
qualquer aplicação de ponto-de-venda pode invocar funções SAT, desde que seja
capaz de fazer requisições HTTP simples.

Também fornece um *frontend* web leve para tornar possível o acesso às funções
do equipamento SAT a partir de um navegador com suporte à HTML5.

.. image:: https://raw.github.com/base4sistemas/sathub/master/doc/static/screenshots/20150919/composicao.png
    :alt: Capturas de tela da aplicação SATHub.
    :align: center

Este projeto integra os projetos `SATCFe`_ e `SATcomum`_ para fornecer uma API
RESTful. Se o seu projeto já for baseado no projeto **SATCFe**, basta configurar
o acesso ao servidor **SATHub** e instanciar :class:`satcfe.ClienteSATHub` ao
invés de instanciar :class:`satcfe.ClienteSATLocal`.

Projetos Relacionados
---------------------

Este projeto é apenas uma parte de um total de cinco projetos que compõem uma
solução compreensível para a tecnologia SAT-CF-e em linguagem Python,
disponíveis para integração nas aplicações de ponto-de-venda. São eles:

* Projeto `SATComum`_
    Mantém o código que é compartilhado pelos outros projetos relacionados,
    tais como validação, formatação e valores constantes.

* Projeto `SATCFe`_
    Fornece acesso ao equipamento SAT diretamente ou através de uma API RESTful,
    quando o equipamento SAT é compartilhado com mais de um ponto-de-venda.

* Projeto `SATExtrato`_
    Impressão dos extratos do CF-e-SAT. Este projeto é capaz de imprimir
    extratos de documentos de venda ou de cancelamento diretamente a partir dos
    documentos XML que os representam. A impressão tem um alto grau de
    compatibilidade com mini-impressoras (conhecidas como impressoras
    não-fiscais) já que é baseada na tecnologia Epson |copy| ESC/POS |reg|
    através do projeto **PyESCPOS**.

* Projeto `PyESCPOS`_
    Implementa o suporte à tecnologia Epson |copy| ESC/POS |reg| compatível com
    a imensa maioria das mini-impressoras disponíveis no mercado.


Participe
---------

Participe deste projeto ou de qualquer um dos projetos relacionados. Se você for
capaz de contribuir com código, excelente! Faça um clone do repositório,
modifique o que acha que deve e faça o *pull-request*. Teremos
`prazer <https://www.python.org/dev/peps/pep-0008/>`_ em
`aceitar <http://docs.python-guide.org/en/latest/writing/style/>`_ o seu
`código <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html>`_.

Se você não quer (ou não pode) programar, também pode contribuir com
documentação. Ou ainda, se você vir algo errado ou achar que algo não está
certo, `conte pra gente <https://github.com/base4sistemas/satcfe/issues>`_.

Siga-nos no `Github <https://github.com/base4sistemas>`_ ou no
`Twitter <https://twitter.com/base4sistemas>`_.

Conteúdo
========

.. toctree::
   :maxdepth: 2

   desenvolvimento
   producao

Tabelas e Índices
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: referencias.rst
