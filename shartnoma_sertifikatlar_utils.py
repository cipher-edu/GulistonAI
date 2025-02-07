from core.models import Shartnoma

# Shartnoma va sertifikatlari
shartnoma = Shartnoma.objects.get(unique_id='some_unique_id')
print(shartnoma.sertifikatlash.all())  # Sertifikatlar bor-yo'qligini tekshirish