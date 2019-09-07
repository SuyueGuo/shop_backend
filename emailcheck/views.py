from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from emailcheck.models import EmailCheck
from designer.models import Designer
from django.http import HttpResponse
import random
from myapp.settings import FROM_EMAIL
import json


server = 'http://127.0.0.1:8000' #服务器域名

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


'''127.0.0.1:8000/emailcheck/?type=register&name=xuchen&email=2017202112@ruc.edu.cn&password=123&telephone=123'''


def emailcheck(request):
    try:
        request_type = request.GET['type']
        if request_type == 'register':
            name = request.GET['name']
            email_address = request.GET['email']
            password = request.GET['password']
            telephone = request.GET['telephone']

            check_designer = Designer.objects.filter(email=email_address)
            if len(check_designer) > 0:
                if check_designer[0].is_active is True:
                    return HttpResponse(json.dumps(dict(request_info='EXIST!'), ensure_ascii=False))
                exist_check = EmailCheck.objects.filter(email=check_designer[0].email)
                if len(exist_check) > 0:
                    exist_check.delete()

            if len(check_designer) == 0:
                designer = Designer()
                designer.name = name
                designer.email = email_address
                designer.password = password
                designer.telephone = telephone
                designer.save()

            email_record = EmailCheck()
            email_record.code = random_str()
            email_record.email = email_address
            email_record.send_type = 'RE'
            email_record.save()

            email_title = '注册激活链接'
            check_link = server + '/emailcheck/?type=register_check&code=' + email_record.code + '&email=' + email_record.email
            email_body = '''<table dir="ltr" class="body" style="border-spacing:0;border-collapse:collapse;vertical-align:top;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;background:#f3f3f3;height:100%;width:100%;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;margin-bottom:0px !important;background-color: white">
      <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <td class="center" align="center" valign="top" style="word-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto;vertical-align:top;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse !important">
          <center style="width:100%;min-width:580px">
            
            
              <table class="container" style="border-spacing:0;border-collapse:collapse;padding:0;vertical-align:top;background:#fefefe;width:580px;margin:0 auto;text-align:inherit;max-width:580px;">
            
              <tbody><tr style="padding:0;vertical-align:top;text-align:left">
                <td style="word-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto;vertical-align:top;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse !important">
                  <div>
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
    <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
    </th>
  </tr>
</tbody></table>
</div>
<div>
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
    <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
      <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
        您好！
      </p>
    </th>
  </tr>
</tbody></table>
</div>
<div>
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
    <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
      <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
        要完成邮箱验证，请在下方确认您的电子邮件地址：
      </p>
    </th>
  </tr>
</tbody></table>
</div>
<div style="padding-top:8px">
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr style="padding:0;vertical-align:top;text-align:left">
    <th class="col-pad-left-2 col-pad-right-2" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;padding-left:16px;padding-right:16px">
      <a href="''' + check_link + '''" class="btn-primary btn-md btn-rausch" style="font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;margin:0;text-align:left;line-height:1.3;color:#2199e8;text-decoration:none;background-color:rgba(0,0,0,0.7);-webkit-border-radius:4px;border-radius:4px;display:inline-block;padding:12px 24px 12px 24px;" rel="noopener" target="_blank">
        <p class="text-center" style="font-weight:normal;padding:0;margin:0;text-align:center;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:white;font-size:18px;line-height:26px;margin-bottom:0px !important;">
          确认电子邮件地址
        </p>
      </a>
    </th>
  </tr>
</tbody></table>
</div>
<div style="padding-top:24px">
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
    <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
      <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
谢谢！<br>不染国潮团队      </p>
    </th>
  </tr>
</tbody></table>
</div>
<div style="padding-top:40px">
<table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
  <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
    <th class="columns first large-12 last small-12 standard-footer-padding" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
      <div class="">
        <hr class="standard-footer-hr" style="max-width:580px;border-right:0;border-top:0;border-bottom:1px solid #cacaca;border-left:0;clear:both;background-color:#dbdbdb;height:2px;width:100%;border:none;margin:auto">
        <div class="row-pad-bot-4" style="padding-bottom:32px">
        </div>
        <p class="standard-footer-text " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
        </p>
        <p class="standard-footer-text center " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
          不染国潮 ♥
        </p>
        <p class="standard-footer-text " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
        </p>
      </div>
    </th>
  </tr>
</tbody></table>
</div>
                </td>
              </tr>
            </tbody></table>
          </center>
        </td>
      </tr>
    </tbody></table>'''
            msg = EmailMessage(email_title, email_body, FROM_EMAIL, [email_record.email])
            msg.content_subtype = 'html'
            msg.send()
            return HttpResponse(json.dumps(dict(request_info='SUCCESS!'), ensure_ascii=False))
        elif request_type == 'register_check':
            code = request.GET['code']
            email_address = request.GET['email']

            thischeck = EmailCheck.objects.filter(code=code)
            if len(thischeck) == 0:
                return HttpResponse(json.dumps(dict(request_info='NOT EXIST!'), ensure_ascii=False))
            else:
                length = len(thischeck)
                for i in range(length):
                    if email_address == thischeck[i].email and 'RE' == thischeck[i].send_type:
                        designer = Designer.objects.filter(email=email_address)
                        designer.update(is_active=True)
                        thischeck[i].delete()
                        return HttpResponse(json.dumps(dict(request_info='SUCCESS!'), ensure_ascii=False))

                return HttpResponse(json.dumps(dict(request_info='NOT EXIST!'), ensure_ascii=False))
        elif request_type == 'forget_pass':
            email_address = request.GET['email']
            password = request.GET['password']

            check_designer = Designer.objects.filter(email=email_address)
            if len(check_designer) == 0:
                return HttpResponse(json.dumps(dict(request_info='NOT EXIST!'), ensure_ascii=False))

            email_record = EmailCheck()
            email_record.code = random_str()
            email_record.email = email_address
            email_record.send_type = 'FG'
            email_record.save()

            email_title = '找回密码链接'
            check_link = server + '/emailcheck/?type=find_pass&code=' + email_record.code + '&email=' + email_record.email + '&password=' + password
            email_body = '''<table dir="ltr" class="body" style="border-spacing:0;border-collapse:collapse;vertical-align:top;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;background:#f3f3f3;height:100%;width:100%;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;margin-bottom:0px !important;background-color: white">
                  <tbody><tr style="padding:0;vertical-align:top;text-align:left">
                    <td class="center" align="center" valign="top" style="word-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto;vertical-align:top;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse !important">
                      <center style="width:100%;min-width:580px">


                          <table class="container" style="border-spacing:0;border-collapse:collapse;padding:0;vertical-align:top;background:#fefefe;width:580px;margin:0 auto;text-align:inherit;max-width:580px;">

                          <tbody><tr style="padding:0;vertical-align:top;text-align:left">
                            <td style="word-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto;vertical-align:top;color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse !important">
                              <div>
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
                <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
                </th>
              </tr>
            </tbody></table>
            </div>
            <div>
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
                <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
                  <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
                    您好！
                  </p>
                </th>
              </tr>
            </tbody></table>
            </div>
            <div>
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
                <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
                  <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
                    请点击下面的按钮以确认修改密码：
                  </p>
                </th>
              </tr>
            </tbody></table>
            </div>
            <div style="padding-top:8px">
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr style="padding:0;vertical-align:top;text-align:left">
                <th class="col-pad-left-2 col-pad-right-2" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;padding-left:16px;padding-right:16px">
                  <a href="''' + check_link + '''" class="btn-primary btn-md btn-rausch" style="font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;margin:0;text-align:left;line-height:1.3;color:#2199e8;text-decoration:none;background-color:rgba(0,0,0,0.7);-webkit-border-radius:4px;border-radius:4px;display:inline-block;padding:12px 24px 12px 24px;" rel="noopener" target="_blank">
                    <p class="text-center" style="font-weight:normal;padding:0;margin:0;text-align:center;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:white;font-size:18px;line-height:26px;margin-bottom:0px !important;">
                      确认修改密码
                    </p>
                  </a>
                </th>
              </tr>
            </tbody></table>
            </div>
            <div style="padding-top:24px">
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
                <th class="columns first large-12 last small-12" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
                  <p class="body  body-lg  body-link-rausch light text-left   " style="padding:0;margin:0;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;font-weight:300;color:#484848;hyphens:none;-moz-hyphens:none;-webkit-hyphens:none;-ms-hyphens:none;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px !important;">
            谢谢！<br>不染国潮团队      </p>
                </th>
              </tr>
            </tbody></table>
            </div>
            <div style="padding-top:40px">
            <table class="row" style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;position:relative;display:table">
              <tbody><tr class="" style="padding:0;vertical-align:top;text-align:left">
                <th class="columns first large-12 last small-12 standard-footer-padding" style="color:#0a0a0a;font-family:'Cereal', Helvetica, Arial, sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
                  <div class="">
                    <hr class="standard-footer-hr" style="max-width:580px;border-right:0;border-top:0;border-bottom:1px solid #cacaca;border-left:0;clear:both;background-color:#dbdbdb;height:2px;width:100%;border:none;margin:auto">
                    <div class="row-pad-bot-4" style="padding-bottom:32px">
                    </div>
                    <p class="standard-footer-text " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
                    </p>
                    <p class="standard-footer-text center " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
                      不染国潮 ♥
                    </p>
                    <p class="standard-footer-text " style="padding:0;margin:0;text-align:left;margin-bottom:10px;font-family:&quot;Cereal&quot;, &quot;Helvetica&quot;, Helvetica, Arial, sans-serif;color:#9ca299;font-size:14px;text-shadow:0 1px #fff;font-weight:300;line-height:1.4">
                    </p>
                  </div>
                </th>
              </tr>
            </tbody></table>
            </div>
                            </td>
                          </tr>
                        </tbody></table>
                      </center>
                    </td>
                  </tr>
                </tbody></table>'''
            msg = EmailMessage(email_title, email_body, FROM_EMAIL, [email_record.email])
            msg.content_subtype = 'html'
            msg.send()
            return HttpResponse(json.dumps(dict(request_info='SUCCESS!'), ensure_ascii=False))
        elif request_type == 'find_pass':
            code = request.GET['code']
            email_address = request.GET['email']
            password = request.GET['password']

            thischeck = EmailCheck.objects.filter(code=code)
            if len(thischeck) == 0:
                return HttpResponse(json.dumps(dict(request_info='NOT EXIST!'), ensure_ascii=False))
            else:
                length = len(thischeck)
                for i in range(length):
                    if email_address == thischeck[i].email and 'FG' == thischeck[i].send_type:
                        designer = Designer.objects.filter(email=email_address)
                        designer.update(password=password)
                        thischeck[i].delete()
                        return HttpResponse(json.dumps(dict(request_info='SUCCESS!'), ensure_ascii=False))

                return HttpResponse(json.dumps(dict(request_info='NOT EXIST!'), ensure_ascii=False))
        else:
            return HttpResponse(json.dumps(dict(request_info='WRONG TYPE!'), ensure_ascii=False))
    except Exception as e:
        return HttpResponse(json.dumps(dict(request_info=str(e) + '<br>' + 'ERROR!'), ensure_ascii=False))
