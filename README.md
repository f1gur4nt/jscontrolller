# jscontrolller

CONFIGURAÇÃO

Voce precisa criar uma conta no ideone e colocar seu username, senha e link no arquivo config.json. Vou ensinar como faz passo-a-passo:

1- vá para https://ideone.com/account/register, se registre tudo bunitinho e confirme sua conta clicando no link que vc recebeu pelo e-mail.
<br>2- Clocando no link do e-mail, vc será enviado para a pagina de login. Faça login usando suas credenciais.
<br>3- Em https://ideone.com/account/, clique em "new code". Após isso, vc será enviando pra um pagina com um código em java. clique no botão escrito "ideone it!".
<br>4- Você será enviado para uma pagina cuja url se assemelha com essa: https://ideone.com/00DihY. Copie o código da sua url. No meu caso é "00DihY".

Após isso, abra o arquivo config.json que estará assim:

{"username":"","password":"","link":""}
  
e subistitua os parametros para as informações da sua conta. ex:
  
{"username":"seuusuario","password":"suasenha","link":"00DihY"}
  
no caso, o "00DihY" seria - Você entendeu. vc não caiu da rede quando criança, né?
  
e salve o arquivo.
  
Em seguida, abra um terminal e execute o seu ngrok assim: ngrok http 8080
  
depois, abra mais outro terminal e execute o jscontroller.py.
  
  
  
Se tudo der certo, aparecerá isso:
  
[*] Editing ideone url ...<br>
[+] Ideone edited as success. jscontroller clients will connect soo.
  
  
Por agora é só isso. Depois eu ensino como gerar a extensão maliciosa pra controlar o browser das vitimas.


