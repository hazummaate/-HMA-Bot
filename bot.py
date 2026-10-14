import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8640092123:AAH-kD9otRMWBVYx120pX851J3cd65SEDME"

# متغيرات حالة البوت
bot_active = True

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active
    
    # قائمة المستخدمين العاديين
    keyboard = [
        [InlineKeyboardButton("📦 إضافة صفقة جديدة (للموردين)", callback_data='add_deal')],
        [InlineKeyboardButton("🔍 تصفح الصفقات المتاحة", callback_data='view_deals')],
        [InlineKeyboardButton("💳 طرق دفع العمولة (فودافون كاش / إنستاباي)", callback_data='payment_info')],
        [InlineKeyboardButton("📜 الشروط وإخلاء المسؤولية", callback_data='disclaimer')]
    ]
    
    # زر إضافي للأدمن (لوحة التحكم)
    keyboard.append([InlineKeyboardButton("⚙️ لوحة تحكم الأدمن (HMA)", callback_data='admin_panel')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "مرحباً بك في منصة **HMA TradeHub** 🤝\n"
        "المنصة الأولى لوساطة وتأمين صفقات الأجهزة المنزلية وقطع الغيار بالجملة.\n\n"
        "يرجى اختيار الخدمة المطلوبة من الأزرار أدناه:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active
    query = update.callback_query
    await query.answer()

    if query.data == 'add_deal':
        if not bot_active:
            await query.edit_message_text("⚠️ البوت حالياً في فترة صيانة/تحديث مؤقتة، يرجى المحاولة لاحقاً.")
            return
            
        await query.edit_message_text(
            "📝 **إضافة صفقة جديدة:**\n\n"
            "يرجى إرسال تفاصيل الصفقة في رسالة واحدة (نوع الجهاز/قطع الغيار، الكمية، السعر المطلوب، المكان).\n\n"
            "⚠️ **تنبيه هام:** يُمنع كتابة أي أرقام هواتف أو وسائل تواصل هنا لضمان حقوق الوساطة.",
            parse_mode='Markdown'
        )
    elif query.data == 'view_deals':
        await query.edit_message_text(
            "🔍 **الصفقات المتاحة حالياً:**\n\n"
            "يمكنك متابعة أحدث الصفقات الحصرية واللوطات المتاحة فوراً عبر قناتنا الرسمية:\n"
            "👉 @HMAGlobalDeals\n\n"
            "عند إعجابك بأي صفقة، أرسل رقم الصفقة هنا لحجزها وتأكيد الربط.",
            parse_mode='Markdown'
        )
    elif query.data == 'payment_info':
        await query.edit_message_text(
            "💳 **طرق سداد العمولة والجدية:**\n\n"
            "• **InstaPay / Vodafone Cash:** (تواصل مع الأدمن لتأكيد رقم المحفظة)\n\n"
            "بعد التحويل، قم بإرسال صورة الإشعار (الاسكرين شوت) هنا لتأكيد الربط بينك وبين المورد/المشتري فوراً.",
            parse_mode='Markdown'
        )
    elif query.data == 'disclaimer':
        await query.edit_message_text(
            "📜 **إخلاء المسؤولية والسياسة القانونية:**\n\n"
            "منصة HMA TradeHub هي منصة وساطة وإعلان جاد للربط بين التجار.\n"
            "• المنصة غير مسؤولة عن جودة البضائع أو الشحن، وتقتصر مسؤوليتنا على الربط الأمين والآمن بين الطرفين.\n"
            "• المعاينة والتسلم يتمان بمعرفة المشتري والمورد مباشرة.",
            parse_mode='Markdown'
        )
    elif query.data == 'admin_panel':
        status_str = "مفعل 🟢" if bot_active else "متوقف مؤقتاً 🔴"
        admin_keyboard = [
            [InlineKeyboardButton(f"تغيير حالة البوت (الحالية: {status_str})", callback_data='toggle_bot')],
            [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='main_menu')]
        ]
        await query.edit_message_text(
            f"⚙️ **لوحة تحكم الأدمن (HMA):**\n\nحالة البوت الحالية: **{status_str}**\nيمكنك إيقاف البوت أو تشغيله بزر واحد.",
            reply_markup=InlineKeyboardMarkup(admin_keyboard),
            parse_mode='Markdown'
        )
    elif query.data == 'toggle_bot':
        bot_active = not bot_active
        status_str = "مفعل 🟢" if bot_active else "متوقف مؤقتاً 🔴"
        await query.edit_message_text(
            f"تم تغيير حالة البوت بنجاح! الحالة الجديدة: **{status_str}**",
            parse_mode='Markdown'
        )
    elif query.data == 'main_menu':
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_active:
        await update.message.reply_text("⚠️ البوت حالياً في حالة توقف مؤقت للتحسينات. سنعود للعمل قريباً!")
        return

    auto_reply = (
        "✅ **تم استلام رسالتك وتفاصيل طلبك بنجاح!**\n\n"
        "جاري مراجعة البيانات من قبل إدارة منصة **HMA TradeHub**.\n"
        "سيتم التواصل معك أو نشر الصفقة فور تأكيد البيانات وفقاً للشروط.\n\n"
        "شكرًا لثقتك بنا! 🤝"
    )
    await update.message.reply_text(auto_reply, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()
