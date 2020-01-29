import traceback
from mimetypes import guess_type
from os.path import basename
from time import time

from behave.model import Feature, Scenario, Step
from reportportal_client import ReportPortalServiceAsync


class ReportPortalManager:
    service: ReportPortalServiceAsync

    valid_batteries = ['smoke', 'full', 'develop']
    endpoint: str
    project: str
    token: str
    launch_name = "[{battery}] {product} {so} "
    launch_doc = "{product} V:{version}{build_version} {browser} {build_url}"

    @staticmethod
    def timestamp() -> str:
        """
        :return:
            str: timestamp convertido em str para uso nos relatorios
        """
        return
        return str(int(time() * 1000))

    @staticmethod
    def error_handler(exc_info):
        """
        Método paradão para gerenciar erros nas chamadas do Report Portal.
        :param exc_info:
            Exception responsavel pelo tratamento do erro.
        """
        return
        print("Error occurred: {}".format(exc_info[1]))
        traceback.print_exception(*exc_info)

    @staticmethod
    def format_traceback(step_traceback) -> str:
        """
        Concatena os erros do step para enviar ao Report Portal.
        :param step_traceback:
            Traceback contendo o erro.
        :return:
            str: Traceback convertida em string.
        """
        return
        val = ''
        for tb in traceback.format_tb(step_traceback):
            val += tb
        return val

    @staticmethod
    def create_attachment(path: str, name: str = None) -> dict:
        """
        Retorna um objeto de anexo pronto para ser enviado ao report portal.
        :param name:
            str: Nome do arquivo
        :param path:
            str: Caminho local ate o arquivo
        :return:
            dict: Objeto pronto para ser enviado ao seridor.
        """
        return
        with open(path, 'rb') as file:
            attachment = {
                "name": basename(path) if not name else name,
                "data": file.read(),
                "mime": guess_type(path)[0] or "application/octet-stream"
            }
        return attachment

    def __init__(self, launch_name: str, launch_doc: str, endpoint: str,
                 token: str, project: str):
        """
        Cria o gerenciador do processo de relatorios.
        :param launch_name:
            str: Nome do Launch
        :param launch_doc:
            str: Documentação do Launch
        :param endpoint:
            str: ReportPortal endpoint
        :param token:
            str: Auth token
        :param project:
            str: Nome do projeto
        """
        self.launch_name = launch_name
        self.launch_doc = launch_doc
        self.endpoint = endpoint
        self.project = project
        self.token = token
        return
        try:
            self.service = ReportPortalServiceAsync(
                endpoint=self.endpoint,
                project=self.project,
                token=self.token,
                error_handler=self.error_handler
            )
        except:
            print('Report Portal is having issues, please check your server.')

    def start_service(self):
        """
        Inicializa um novo serviço para a bateria de testes no Report Portal.
        """
        return
        try:
            self.service.start_launch(name=self.launch_name,
                                      start_time=self.timestamp(),
                                      description=self.launch_doc)
        except:
            pass

    def start_feature(self, feature: Feature):
        """
        Inicializa um novo teste de feature.
        Itens validos para o test_item (SUITE, STORY, TEST, SCENARIO, STEP,
        BEFORE_CLASS, BEFORE_GROUPS, BEFORE_METHOD, BEFORE_SUITE, BEFORE_TEST,
        AFTER_CLASS, AFTER_GROUPS, AFTER_METHOD, AFTER_SUITE, AFTER_TEST)
        :param feature:
            Objeto da feature utilizada no teste.
        """
        return
        try:
            self.service.start_test_item(name=feature.name,
                                         description=f'{feature.description}',
                                         tags=feature.tags,
                                         start_time=self.timestamp(),
                                         item_type="STORY")
        except:
            pass

    def start_scenario(self, scenario: Scenario):
        """
        Inicializa um novo cenario de testes.
        Itens validos para o test_item (SUITE, STORY, TEST, SCENARIO, STEP,
        BEFORE_CLASS, BEFORE_GROUPS, BEFORE_METHOD, BEFORE_SUITE, BEFORE_TEST,
        AFTER_CLASS, AFTER_GROUPS, AFTER_METHOD, AFTER_SUITE, AFTER_TEST)
        :param scenario:
            Objeto scenario utilizado no teste
        """
        return
        try:
            self.service.start_test_item(name=scenario.name,
                                         description=f'{scenario.description}',
                                         tags=scenario.tags,
                                         start_time=self.timestamp(),
                                         item_type="SCENARIO")
        except:
            print('Report Portal is having issues, please check your server.')

    def start_step(self, step: Step, attachment=None):
        """
        Cria um log relativo ao step realizado.
        :param step:
            Objeto step utilizado no teste.
        :param attachment:
            dict/str: anexo a ser enviado ao servidor.
        """
        return
        try:
            self.service.log(time=self.timestamp(),
                             message=f"{step.name}[:{step.line}] - Has started...",
                             attachment=attachment,
                             level="INFO")
        except:
            pass

    def finish_step(self, step: Step, message_extras=None, attachment=None):
        """
        Cria um log de finalização de step. Acusando erro ou sucesso, de acordo
        com seu status.
        Atualmente gera um anexo com o um arquivo e envia ao servidor.
        :param step:
            Objeto step utilizado no teste.
        :param message_extras:
            str: adicionar texto extra na corpo da mensagem.
        :param attachment:
            dict/str: anexo a ser enviado ao servidor.
        """
        return
        try:
            status = step.status if type(
                step.status) == str else step.status.name
            if status == 'failed':
                message = (
                        f'{step.name}[:{step.line}] - Has failed...\n' +
                        self.format_traceback(step.exc_traceback)
                )
                level = 'ERROR'
            else:
                message = f"{step.name}[:{step.line}] - Has finished..."
                level = "INFO"

            message += message_extras if message_extras else ''

            allow_attachment = False
            for battery in self.valid_batteries:
                if battery in self.launch_name:
                    allow_attachment = True
                    break

            # Desabilitando temporariamente o uso dos txts para testes de stress.
            if attachment and '.txt' in attachment.name:
                allow_attachment = False

            self.service.log(
                time=self.timestamp(),
                message=message,
                level=level,
                attachment=attachment if allow_attachment else None
            )
        except:
            pass

    def finish_scenario(self, scenario: Scenario):
        """
        Finaliza o cenario de testes atual.
        :param scenario:
            Objeto scenario utilizado no teste
        """
        return
        try:
            status = scenario.status if type(
                scenario.status) == str else scenario.status.name
            self.service.finish_test_item(end_time=self.timestamp(),
                                          status=status)
        except:
            pass

    def finish_feature(self, feature: Feature):
        """
        Finaliza a feature de testes atual.
        :param feature:
            Objeto da feature utilizada no teste.
        """
        return
        try:
            status = feature.status if type(
                feature.status) == str else feature.status.name
            self.service.finish_test_item(end_time=self.timestamp(),
                                          status=status)
        except:
            pass

    def finish_service(self):
        """
        Finaliza o serviço, fecha a conexão com o servidor e conclui a
        bateria de testes.
        """
        return
        try:
            self.service.finish_launch(end_time=self.timestamp())
            self.service.terminate()
        except:
            pass
