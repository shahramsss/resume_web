import os
from io import BytesIO
from django.core.files import File
from django.db import models
from PIL import Image

class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)

    technologies = models.ManyToManyField(Technology)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    # فیلد تصویر را به همان صورت نگه می‌داریم
    image = models.ImageField(upload_to="projects/")
    alt = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # بررسی می‌کنیم که آیا تصویر جدیدی آپلود شده است یا خیر
        if self.image:
            # باز کردن تصویر با استفاده از Pillow
            img = Image.open(self.image)

            # تبدیل مد تصویر به RGB (در صورتی که PNG با کانال آلفا/شفاف باشد)
            if img.mode in ("RGBA", "LA") or (
                img.mode == "P" and "transparency" in img.info
            ):
                # برای حفظ شفافیت می‌توان از فرمت WebP با حفظ آلفا استفاده کرد
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            # تغییر اندازه تصویر در صورت بزرگ بودن (مثلاً حداکثر عرض 1200 پیکسل)
            max_width = 1200
            if img.width > max_width:
                # محاسبه ارتفاع متناسب با عرض جدید برای حفظ نسبت تصویر (Aspect Ratio)
                output_size = (max_width, int((max_width / img.width) * img.height))
                img = img.resize(output_size, Image.Resampling.LANCZOS)

            # ذخیره تصویر در حافظه موقت (BytesIO) برای تبدیل به فرمت کم‌حجم WebP
            output = BytesIO()
            # فشرده‌سازی با کیفیت 80 (مناسب‌ترین نسبت حجم به کیفیت)
            img.save(output, format="WEBP", quality=80)
            output.seek(0)

            # تغییر نام فایل به پسوند .webp
            name = os.path.splitext(self.image.name)[0]
            self.image = File(output, name=f"{name}.webp")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.project.title}"
