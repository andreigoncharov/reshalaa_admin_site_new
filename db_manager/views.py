import asyncio
import re

from aiogram import Bot
from aiogram.types import inline_keyboard
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from .forms import *
from .scripts import *

BOT_TOKEN = '1269877919:AAFxsJ1D5W9HqVqN5lrpLoMTVzdna2cKqIY'
BOT_URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
BOT_CHAT_ID = ''

ABOT_TOKEN = '1269877919:AAFxsJ1D5W9HqVqN5lrpLoMTVzdna2cKqIY'
ABOT_URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
ABOT_CHAT_ID = ''

async def send_message(chat_id, text=None, keyboard=None, token=BOT_TOKEN):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='html')
    return
async def send_message_a(chat_id, text=None, keyboard=None, token=ABOT_TOKEN):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode='html')
    return

async def send_photo(chat_id, photo, token=BOT_TOKEN):
    bot = Bot(token=token)
    await bot.send_photo(chat_id, photo=photo)
    return


async def send_document(chat_id, document, token=BOT_TOKEN):
    bot = Bot(token=token)
    await bot.send_document(chat_id, document=document)
    return


def orderInfo(request):
    order = Order.objects.all()
    return render(request, 'db_manager/orderInfo.html', {'order': order})


def create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wo')

    form = OrderForm()

    data = {
        'form': form
    }
    return render(request, 'db_manager/create.html', data)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'db_manager/order_detail.html'
    context_object_name = 'dorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info = get_ord_auth_price(str(context['object']))
        authors_price = []
        for inf in info:
            a = {'ord_id': inf[0],
                 'auth_username': inf[4],
                 'price': inf[2],
                 'com': inf[3],
                 'tel_id': inf[1]}
            authors_price.append(a)
        context['auth'] = authors_price
        try:
            links = get_links(str(context['auth'][0]), 'db_manager_order')
            links_list = links.split(' , ')
            links = []
            for link in links_list:
                link = str(link).replace(',', '')
                d = {'link': link}
                links.append(d)
            context['links'] = links
            context['phone_num'] = get_customer_info(str(context['object']))[0]
        except:
            context['phone_num'] = get_customer_info(str(context['object']))[0]
            context['links'] = 'Нет ссылок'
        return context


class AOrderDetailView(DetailView):
    model = ActiveO
    template_name = 'db_manager/orderInfo.html'
    context_object_name = 'dorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = get_links(str(context['object']), 'db_manager_activeo')
        links_list = links.split(' , ')
        links = []
        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links'] = links
        return context


class WOrderDetailView(DetailView):
    model = waitO
    template_name = 'db_manager/w_orderInfo.html'
    context_object_name = 'dorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        links, author_links = get_links_plus_author(str(context['object']), 'db_manager_waito')

        links_list = links.split(' , ')
        links = []

        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links'] = links

        links_list = author_links.split(' , ')
        links = []

        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links_a'] = links

        return context


class DorderDetailView(DetailView):
    model = doneO
    template_name = 'db_manager/d_order.html'
    context_object_name = 'dorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links, author_links = get_links_plus_author(str(context['object']), 'db_manager_doneo')

        links_list = links.split(' , ')
        links = []

        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links'] = links

        links_list = author_links.split(' , ')
        links = []

        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links_a'] = links

        return context


class CorderDetailView(DetailView):
    model = canceledo
    template_name = 'db_manager/c_order.html'
    context_object_name = 'dorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        links = get_links(str(context['object']), 'db_manager_canceledo')
        links_list = links.split(' , ')
        links = []
        for link in links_list:
            link = str(link).replace(',', '')
            d = {'link': link}
            links.append(d)
        context['links'] = links
        return context


class OrderUpdateView(UpdateView):
    model = Order
    form_class = UpdateForm
    template_name = 'db_manager/update.html'
    success_url = reverse_lazy('wo')

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_text())

class AOrderUpdateView(UpdateView):
    model = ActiveO
    form_class = AUpdateForm
    template_name = 'db_manager/updatewo.html'
    success_url = reverse_lazy('orderInfo')

    def form_valid(self, form):
        tel_id = get_author(self.request.POST.get('author'))
        text = f'<b>Изменения в заказе!</b>' \
               f'<b>Предмет:</b> {self.request.POST.get("predm")}\n' \
               f'<b>Тип работы:</b> {self.request.POST.get("type")}\n\n' \
               f'Срок сдачи: {self.request.POST.get("date")} ' \
               f'\n{self.request.POST.get("time")}\n' \
               f'Оформление:{self.request.POST.get("oforml")}\n' \
               f'Комментарий: {self.request.POST.get("info")}\n\n' \
               f'Прикрепленные файлы:{self.request.POST.get("links")}'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_message(tel_id, text=text))
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_text())

class WOrderUpdateView(UpdateView):
    model = waitO
    form_class = UpdateForm
    template_name = 'db_manager/updatewo.html'
    success_url = reverse_lazy('waitOh')

class PAYS_UPDATE(UpdateView):
    model = pays
    form_class = PAYS_FORM
    template_name = 'db_manager/bonuses.html'
    success_url = reverse_lazy('wo')

    def form_valid(self, form):
        price_u = self.request.POST.get('price')
        ord_id = self.request.POST.get('ord_id')
        a = str(self.request)
        new_str = a[32:]
        ind = new_str.find('confirmmyprice/')
        auth = new_str[ind+15:-2]

        tel_id = send_price_c_2(ord_id, auth, price_u)
        cost, bonuses = get_new_cost(tel_id, ord_id)

        k = inline_keyboard.InlineKeyboardMarkup()
        k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить 💰', callback_data=f'pay_{ord_id}'))
        k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить c бонусами 💰', callback_data=f'payb_{ord_id}'))
        k.add(inline_keyboard.InlineKeyboardButton('❌ Отменить заказ ❌', callback_data=f'otmena_{ord_id}'))

        price = cost
        p_price = round(int(price) * (50 / 100))

        text = '<b>Мы оценили заказ и готовы его выполнить!</b> 🚀' \
               f'\n<b>Заказ № {ord_id}</b>\n\n' \
               f'➡️ <b>К оплате: {price} грн.</b>  ⬅️\n' \
               f'Для начала работы можно внести предоплату в размере {p_price} грн.\n\n' \
               f'На вашем счету есть бонусы в размере <i>{bonuses}</i> грн. Вы можете их использовать!\n\n' \
               '⚠️ Предложение действительно в течении 24 часов ⚠️'

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_message(tel_id[0], text=text, keyboard=k))

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('wo')
    template_name = 'db_manager/delete_o.html'

class UpdateBonucesView(UpdateView):
    model = Bonuses
    form_class = BonucesUpdateForm
    template_name = 'db_manager/update_bonuces.html'
    success_url = reverse_lazy('users')

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_text())

def delete_order(request):
    ord_id = request.GET.get("id", False)
    tel_id = get_customer_and_delete_order(ord_id)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    text = 'К сожалению, не сможем вам помочь'
    loop.run_until_complete(send_message(tel_id, text=text))
    return render(request, 'db_manager/wo.html')


def restart_order(request):
    ord_id = request.GET.get("id", False)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_new_order(ord_id))
    return render(request, 'db_manager/wo_1.html')


async def send_new_order(ord_id):
    order = get_new_order(ord_id)
    tel_id = order[1]
    user = get_user_t(tel_id)
    text = f'✨ Заказ №{order[0]} ✨\n\n' \
           f'<b>{order[4]}</b>\n' \
           f'<b>{order[2]}</b>\n\n' \
           f'Срок сдачи: {order[7]} {order[8]}\n' \
           f'Цена: {order[10]}\n\n' \
           f'Оформление: {order[6]}\n' \
           f'Комментарий: {order[5]}\n\n' \
           f'ВУЗ: {user[3]}' \
           f'\nПрикрипленные файлы:'
    authors = get_authors(ord_id)
    await send_message(chat_id=493247603, text=text, keyboard=ord_1(order[0]))
    await send_files(tel_id, order[0])
    for author in authors:
        await send_message(chat_id=author[0], text=text, keyboard=ord_1(order[0]))
        await send_files(tel_id, order[0])


async def send_files(tel_id, order_id):
    docs = get_docs(order_id)
    ph = []
    if docs == False:
        await send_message(chat_id=tel_id, text='Нет прикрипленных файлов')
    else:
        for doc in docs:
            if doc[2] == 'photto':
                await send_photo(tel_id, photo=doc[1])
            else:
                await send_document(tel_id, document=doc[1])


def ord_1(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Оценить 💰', callback_data=f'otzenit_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('Не интересно 🗑', callback_data=f'nint_{ord_id}'))

    return k


def confirm_price(request):
    ord_id = request.GET.get("id", False)
    data = ord_id.split('?')
    ord_id = data[0]
    auth = data[1].replace('auth=', '')
    name = request.GET.get('name')

    tel_id = send_price_c(ord_id, auth)
    cost, bonuses = get_new_cost(tel_id, ord_id)

    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить 💰', callback_data=f'pay_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('💰Оплатить c бонусами 💰', callback_data=f'payb_{ord_id}'))
    k.add(inline_keyboard.InlineKeyboardButton('❌ Отменить заказ ❌', callback_data=f'otmena_{ord_id}'))

    price = cost
    p_price = round(int(price) * (50 / 100))

    text = '<b>Мы оценили заказ и готовы его выполнить!</b> 🚀' \
           f'\n<b>Заказ № {ord_id}</b>\n\n' \
           f'➡️ <b>К оплате: {price} грн.</b>  ⬅️\n' \
           f'Для начала работы можно внести предоплату в размере {p_price} грн.\n\n' \
           f'На вашем счету есть бонусы в размере <i>{bonuses}</i> грн. Вы можете их использовать!\n\n' \
           '⚠️ Предложение действительно в течении 24 часов ⚠️'

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message(tel_id[0], text=text, keyboard=k))

    return render(request, 'db_manager/wo_1.html')

class confirm_2(DetailView):
    model = pays
    form_class = PAYS_FORM
    template_name = 'db_manager/bonuces.html'
    success_url = reverse_lazy('wo')

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_text())

def bonuses(request, pk):
    set_b_count_tel_id(pk)

    return render(request, 'db_manager/bonuses.html')

def bonuses_set(request):

    authors = for_users()
    authors_list = []
    for author in authors:
        d = {'name': author[1],
             'link': f'https://t.me/{author[5]}',
             'phone': author[2],
             'vuz': author[3],
             'tel_id': author[0]}
        authors_list.append(d)
    return render(request, 'db_manager/users.html', {'authors': authors_list})

def confandsend(request):
    ord_id = request.GET.get("id", False)
    data = ord_id.split('?')
    ord_id = data[0]

    payment, tel_id, files = check_and_send_order(ord_id)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    k = inline_keyboard.InlineKeyboardMarkup()
    k.add(inline_keyboard.InlineKeyboardButton('Связь с менеджером 📱', callback_data='manager'))

    if payment == 1:
        text = f'🎊 <b>Ваша робота готова!</b> 🎊\n' \
               f'Заказ №{ord_id}'
        loop.run_until_complete(send_message(tel_id, text=text))

        file = files.split(' , ')
        for f in file:
            if f == '':
                a = ''
            else:
                loop.run_until_complete(send_message(tel_id, text=f))

        text_2 = '❤️ <b>Спасибо, что вы с Reshalla</b>\n' \
                 ' ❤️<b>Желаем удачи со сдачей работы!</b>\n' \
                 'Есть вопросы? 👇'
        loop.run_until_complete(send_message(tel_id, text=text_2, keyboard=k))

        text_3 = '<b>Насколько Вы довольны нашей работой?</b>\n' \
                 'Выберите цифру от 1 до 5	🙌'
        loop.run_until_complete(send_message(tel_id, text=text_3, keyboard=otz(ord_id)))

    else:
        text = f'<b>Ваш заказ №{ord_id} готов!\n\n</b>' \
               f'❗️Пожалуйста, внесите доплату, чтобы получить готовую работу\n️' \
               f'➡️ <b>К доплате: {payment} грн.</b>  ⬅️'
        k1 = inline_keyboard.InlineKeyboardMarkup()
        k1.add(inline_keyboard.InlineKeyboardButton('💰Оплатить 💰', callback_data=f'paytwo_{ord_id}'))
        loop.run_until_complete(send_message(tel_id, text=text, keyboard=k1))
    return render(request, 'db_manager/wo_1.html')


def otz(ord_id):
    k = inline_keyboard.InlineKeyboardMarkup()
    one = inline_keyboard.InlineKeyboardButton('1️⃣', callback_data=f'one_{ord_id}')
    two = inline_keyboard.InlineKeyboardButton('2️⃣', callback_data=f'two_{ord_id}')
    three = inline_keyboard.InlineKeyboardButton('3️⃣', callback_data=f'three_{ord_id}')
    four = inline_keyboard.InlineKeyboardButton('4️⃣', callback_data=f'four_{ord_id}')
    five = inline_keyboard.InlineKeyboardButton('5️⃣', callback_data=f'five_{ord_id}')
    k.row(one, two, three, four, five)
    return k


def payok(request):
    ord_id = request.GET.get("id", False)
    data = ord_id.split('?')
    ord_id = data[0]

    payok_db(ord_id)
    order = Order.objects.all()

    return render(request, 'orders/wo.html', {'order': order})


def index(request):
    wait, price, active, prov = for_start()
    return render(request, 'db_manager/first_page.html', {'wait': wait,
                                                          'price': price,
                                                          'active': active,
                                                          'prov': prov})


def wo(request):
    order = Order.objects.all()
    st = str(order)
    st = st.split(',')
    nums = []
    n = []
    for s in st:
        nums.append(re.findall(r'\d+', s))
    for num in nums:
        n.append(num)
    nums.clear()
    for num in n:
        try:
            count = get_authors_count(num[0])
            nums.append(count)
        except:
            nums.append(0)
    full_dict = {'order': order, 'count': nums}
    return render(request, 'orders/wo.html', context=full_dict)


def priceO(request):
    order = cust_pri.objects.all()
    return render(request, 'db_manager/priceO.html', {'order': order})


def authors(request):
    authors = for_authors()
    authors_list = []
    for author in authors:
        d = {'link': f'https://t.me/{author[9]}',
             'phone': author[1],
             'predm': author[8],
             'card_num': author[6],
             'vuz': author[3],
             'step': author[4]}
        authors_list.append(d)
    return render(request, 'db_manager/authors.html', {'authors': authors_list})


def users(request):
    authors = for_users()
    authors_list = []
    for author in authors:
        d = {'name': author[1],
             'link': f'https://t.me/{author[5]}',
             'phone': author[2],
             'vuz': author[3],
             'tel_id': author[0]}
        authors_list.append(d)
    return render(request, 'db_manager/users.html', {'authors': authors_list})


def wo_1(request):
    order = Order.objects.all()
    st = str(order)
    st = st.split(',')
    nums = []
    n = []
    for s in st:
        nums.append(re.findall(r'\d+', s))
    for num in nums:
        n.append(num)
    nums.clear()
    for num in n:
        count = get_authors_count(num[0])
        nums.append(count)
    full_dict = {'order': order, 'count': nums}
    return render(request, 'db_manager/wo_1.html', context=full_dict)


def activeO(request):
    orders = ActiveO.objects.all()
    return render(request, 'orders/activeO.html', {'order': orders})


def canceledO(request):
    orders = canceledo.objects.all()
    return render(request, 'orders/canceledO.html', {'order': orders})


def waitOh(request):
    order = waitO.objects.all()
    return render(request, 'orders/waitOh.html', {'order': order})


def DpO(request):
    info = get_authors_balance()
    result = []
    for author in info:
        balance = author[12]
        if balance is None or balance == 0:
            d = None
        else:
            a = {'username': author[9],
                 'card': author[6],
                 'balance': balance}
            result.append(a)
    return render(request, 'orders/pay.html', {'info': result})


def DoneO(request):
    order = doneO.objects.all()
    return render(request, 'orders/doneO.html', {'order': order})


class ActiveOrderDetailView(DetailView):
    model = ActiveO
    template_name = 'db_manager/orderInfo.html'
    context_object_name = 'dorder'

#            <a href="{% url 'create' %}"><li><button class="btn btn-info"><i class="fas fa-plus-circle"> Добавить заказ</i></button></li></a>
