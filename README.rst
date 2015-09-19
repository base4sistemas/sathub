
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

Também fornece um *frontend* web leve para tornar possível o acesso às funções
do equipamento SAT a partir de um navegador com suporte à HTML5.

.. image:: https://raw.github.com/base4sistemas/sathub/master/doc/static/screenshots/20150919/composicao.png
    :align: center
    :alt: Capturas de tela da aplicação SATHub.

Este projeto integra os projetos `SATCFe <https://github.com/base4sistemas/satcfe>`_ e
`SATcomum <https://github.com/base4sistemas/satcomum>` para fornecer uma API
RESTful. Se o seu projeto já for baseado no projeto **SATCFe**, basta configurar
o acesso ao servidor SATHub e instanciar ``satcfe.ClienteSATHub`` ao invés de
instanciar ``satcfe.ClienteSATLocal``.


Instalando em Modo de Desenvolvimento no Windows 8.1
====================================================

Caso queira experimentar SATHub em Windows, o roteiro não é exatamente curto mas
é bem simples. O primeiro passo é instalar o `Python`_ 2.7 e todas as demais
dependências para que seja possível executar o servidor SATHub em modo de
desenvolvimento.

#. Baixe o arquivo MSI para sua arquitetura `neste link <https://www.python.org/downloads/windows/>`_.
   Procure o link *Latest Python 2 Release* e então localize o link para para o
   pacote **Windows x86 MSI installer** ou **Windows x86-64 MSI installer** se
   a arquitetura do seu sistema for 64 bits. Faça a instalação normalmente como
   qualquer outro pacote MSI, aceitando as opções pré-definidas.

#. Para ter acesso aos binários, será preciso incluir o caminho em ``Path``.
   Tecle ``Win+X`` e escolha a opção *Sistema*.

#. No diálogo *Sistema* escolha a opção *Configurações avançadas do sistema*.

#. No diálogo *Propriedades do Sistema*, guia *Avançado*, clique no botão
   *Variáveis de Ambiente*.

#. Na lista de *Variáveis do Sistema* localize a variável ``Path``, selecione-a
   e clique em *Editar* e **inclua** (não apague o valor já existente) o
   seguinte trecho no início do campo *Valor*::

        C:\Python27;C:\Python27\Scripts;

   Se você instalou o Python em um caminho diferente, adapte os valores.

#. Abra o Windows PowerShell: mova o cursor para o canto superior direito,
   clique na opção *Pesquisar* e escreva ``powershell``. A primeira opção
   encontrada deverá ser *Windows PowerShell*, clique nela.

#. Digite o seguinte comando no terminal:

   .. sourcecode:: powershell

        PS C:\Users\User> python --version
        Python 2.7.10

   Se obtiver um erro, revise os passos.

Com o Python instalado será preciso instalar as dependências para execução
do SATHub em modo de desenvolvimento. Ainda no Windows PowerShell:

.. sourcecode:: powershell

    PS C:\Users\User> pip install virtualenv
    PS C:\Users\User> virtualenv sat
    PS C:\Users\User> .\sat\Scripts\activate.ps1
    (sat) PS C:\Users\User> pip install flask
    (sat) PS C:\Users\User> pip install flask-restful
    (sat) PS C:\Users\User> pip install unidecode
    (sat) PS C:\Users\User> pip install requests
    (sat) PS C:\Users\User> pip install satcomum
    (sat) PS C:\Users\User> pip install satcfe

Faça o `download dos fontes <https://github.com/base4sistemas/sathub/archive/master.zip>`_
do projeto SATHub (ou clone o projeto se você possui o
`Git <https://git-scm.com/download/win>`_ instalado) e descompacte o arquivo em
um diretório de sua preferência, digamos ``C:\workdir``.

.. sourcecode:: powershell

    (sat) PS C:\Users\User> cd \workdir\sathub-master\
    (sat) PS C:\workdir\sathub-master> python runserver.py

Se lhe for apresentando o diálogo de restrição de acesso do Firewall do Windows,
permita o acesso para o aplicativo. Você deverá ver uma saída como essa
(aparentemente com informação duplicada, isso é normal em desenvolvimento):

.. sourcecode:: text

    SATHub versao 0.1
    [-] Debug esta LIGADO
    [-] Caminho para DLL: sat.dll
    [-] Convencao de chamada para DLL: Windows "stdcall"
    ** DLL NAO ENCONTRADA **

     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
     * Restarting with stat
    [-] Debug esta LIGADO
    [-] Caminho para DLL: sat.dll
    [-] Convencao de chamada para DLL: Windows "stdcall"
    ** DLL NAO ENCONTRADA **

Neste ponto o servidor está em execução, mas há um problema. Note a mensagem
que diz **DLL NAO ENCONTRADA**. Interrompa o servidor teclando ``Ctrl+C``.
Note que após a primeira execução foi criado um arquivo chamado ``conf.json``.
Abra esse arquivo com um editor de textos e coloque o caminho completo para a
DLL do seu equipamento SAT. O arquivo deverá ficar mais ou menos assim:

.. sourcecode:: json

    {
        "debug": true,
        "codigo_ativacao": "123456789",
        "convencao_chamada": 2,
        "caminho_dll": "C:/SAT/SAT.DLL"
    }

Note que o caminho para a DLL é especificado usando barras no padrão Unix
(``/`` *forward slahes*), mesmo no Windows, ao invés de usar contra-barras.

Se o seu código de ativação for diferente, altere-o também. A convenção de
chamada ``2`` significa *Windows Standard calls* (ou apenas *Windows StdCall*).
Se sua DLL usar a convenção de chamadas de C (*Standard C calls*) altere a
propriedade ``convencao_chamada`` para ``1``.

Execute o servidor novamente com ``python runserver.py``. Você deverá ver a
seguinte saída.

.. sourcecode:: text

    SATHub versao 0.1
    [-] Debug esta LIGADO
    [-] Caminho para DLL: C:\SAT\SAT.DLL
    [-] Convencao de chamada para DLL: Windows "stdcall"

     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
     * Restarting with stat
    [-] Debug esta LIGADO
    [-] Caminho para DLL: C:\SAT\SAT.DLL
    [-] Convencao de chamada para DLL: Windows "stdcall"


Acessando a API via PowerShell
------------------------------

Neste ponto o servidor está em execução, o caminho para a DLL do equipamento
SAT foi configurado e está tudo OK. Podemos então fazer algumas chamadas à API
do SATHub para vê-lo em ação. Abra outra janela do PowerShell e digite:

.. sourcecode:: powershell

    PS C:\Users\User> Invoke-RestMethod -Uri http://localhost:5000/hub/v1/consultarsat -Method POST -Body "numero_caixa=1"

Na janela do terminal PowerShell em que o servidor está em execução você verá o
acesso à URI, o método de acesso e o código de resposta, ``200`` OK, entre
outras informações::

    127.0.0.1 - - [20/Jun/2015 10:25:48] "POST /hub/v1/consultarsat HTTP/1.1" 200 -

No terminal em que o comando ``Invoke-RestMethod`` foi executado você terá o
seguinte resultado (se tudo correr bem)::

    funcao                    retorno
    ------                    -------
    ConsultarSAT              101341|08000|SAT em operação||

O equivalente em um terminal Linux, usando `curl`_, é o seguinte (acessando a
máquina Windows 8.1 em que o SATHub está executando, como no exemplo acima):

.. sourcecode:: bash

    $ curl --data "numero_caixa=1" http://10.0.0.115:5000/hub/v1/consultarsat
    {
        "funcao": "ConsultarSAT",
        "retorno": "101363|08000|SAT em opera\u00e7\u00e3o||"
    }

Se você tiver outras máquinas Windows em uma rede local, ou estiver usando
máquinas virtuais, você poderá acessar um único equipamento SAT a partir de
qualquer uma delas.


Acessando a API em C#
---------------------

Os exemplos abaixo mostram como é simples acessar a API RESTful de SATHub
através de outras linguagens muito comumente usadas neste campo de aplicações.
Neste exemplo, usando C# (testado com `MonoDevelop`_):

.. sourcecode:: csharp

    // (!) baseado em http://stackoverflow.com/a/4015346/550237
    using System;
    using System.Collections.Specialized;
    using System.Net;
    using System.Text;

    public class ExemploSATHub
    {
        static public void Main()
        {
            Console.WriteLine(ConsultarSAT());
        }

        private static string ConsultarSAT()
        {
            var payload = new NameValueCollection();
            payload["numero_caixa"] = "1";

            var client = new WebClient();
            var response = client.UploadValues(
                    "http://10.0.0.115:5000/hub/v1/consultarsat", payload);

            return Encoding.Default.GetString(response);
        }
    }

O resultado é o seguinte:

.. sourcecode:: bash

    $ msc exemplo.cs
    $ mono exemplo.exe
    {
        "funcao": "ConsultarSAT",
        "retorno": "100914|08000|SAT em opera\u00e7\u00e3o||"
    }


Executando *smoke tests*
========================

Certas funções SAT são difíceis de serem executadas contra um equipamento SAT
real ou até mesmo contra o emulador desenvolvido pela Secretária da Fazenda,
como por exemplo, ``AtualizarSoftwareSAT`` ou ``CancelarUltimaVenda``. Por esse
motivo foi desenvolvido um *mockup* da biblioteca SAT, que implementa todas as
funções que a biblioteca SAT implementa, mas não acessa nenhum equipamento. As
funções apenas recebem os parâmetros esperados e devolvem uma resposta muito
parecida com uma resposta de sucesso. Desse modo, o *mockup* da biblioteca SAT
torna trivial executar testes simples para verificar o comportamento da API.

Para executar os *smoke tests* será necessário compilar o *mockup* da
biblioteca SAT que está em ``sathub/test/mockup/``. Você irá precisar de um
compilador GCC ou outro capaz de compilar o código. Tipicamente, em um ambiente
Linux, basta invocar ``make`` para produzir o arquivo ``libmockupsat.so``.

Configure o SATHub apontando para o *mockup* da biblioteca SAT (normalmente, a
convenção de chamada será *Standard C*, equivalente a ``1``):

.. sourcecode:: json

    {
        "debug": true,
        "codigo_ativacao": "123456789",
        "convencao_chamada": 1,
        "caminho_dll": "~/sathub/test/mockup/libmockupsat.so"
    }

Para executar os testes é necessário instalar o framework para testes de APIs
RESTful **PyRestTest** e suas dependências:

.. sourcecode:: shell

    (sat)$ pip install pyresttest pyyaml pycurl jsonschema

Abra uma janela de terminal e execute o servidor SATHub:

.. sourcecode:: shell

    (sat)$ python runserver.py

Abra uma outra janela do terminal e vá até o diretório onde está o arquivo YAML
que descreve os testes e execute-os com PyRestTest:

.. sourcecode:: shell

    (sat)$ cd ~/sathub/test/tests
    (sat)$ resttest.py http://localhost:5000 smoke.yaml
    Test Group Metodos SAT-CF-e SUCCEEDED: 14/14 Tests Passed!


Considerações
=============

Via de regra, é recomendado que se mantenha um olho na legislação vigente a
respeito da tecnologia SAT-CF-e e das implicações dessa legislação na tecnologia
de suporte empregrada. Atualmente não há nada regulamentando o acesso
compartilhado ao equipamento SAT. Tudo o que se tem é que essa possibilidade tem
sido aventada desde os primórdios do projeto.

Sendo assim, apenas use o bom senso ao compartilhar o acesso ao equipamento SAT
e evite compartilhar muitos pontos-de-venda em único equipamento. Considere
balancear o número de pontos-de-venda e tenha sempre uma folga para redirecionar
em caso de pane em um equipamento, por exemplo.


.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
.. _`satcfe`: https://github.com/base4sistemas/satcfe
.. _`Python`: https://www.python.org/
.. _`Flask`: http://flask.pocoo.org/
.. _`Flask-RESTful`: https://flask-restful.readthedocs.org/
.. _`curl`: http://curl.haxx.se/
.. _`MonoDevelop`: http://www.monodevelop.com/
