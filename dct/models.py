from django.db import models

# Create your models here.

class ModelPenyisipan(models.Model):
	username = models.CharField(max_length=256, null=True)
	nama_img = models.CharField(max_length=256, null=True)
	host_img = models.ImageField(upload_to='embeds/', blank=False, null=False)
	wm_img = models.ImageField(upload_to='watermark/', blank=False, null=False)
	result = models.ImageField(upload_to='result/', blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	psnr = models.FloatField(null=True)
	mse = models.FloatField(null=True)
	embed_id = models.SlugField(null=True)

	def __str__(self):
		return self.embed_id

class ModelPengekstrakan(models.Model):
	username = models.CharField(max_length=256, null=True)
	nama_img = models.CharField(max_length=256, null=True)
	host_img = models.FileField(upload_to='extracts/', blank=False, null=False)
	result = models.ImageField(upload_to='result/', blank=True, null=True)
	ukuran = models.CharField(max_length=256, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	extract_id = models.SlugField(null=True)

	def __str__(self):
		return self.extract_id