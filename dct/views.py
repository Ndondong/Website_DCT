from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone

from PIL import Image
from io import BytesIO
from pathlib import Path

from .forms import FormPenyisipan, FormPengekstrakan, RegisterForm
from .validators import *
from .dct import *
from .models import *
from .tables import *

# Create your views here.
def Dashboard(request):
	if not request.user.is_authenticated:
		return redirect('login')

	today = timezone.now().date()
	penyisipan = ModelPenyisipan.objects.all().count()
	pengekstrakan = ModelPengekstrakan.objects.all().count()
	penyisipan_td = ModelPenyisipan.objects.filter(timestamp__date=today).count()
	pengekstrakan_td = ModelPengekstrakan.objects.filter(timestamp__date=today).count()
	context = {
		'page': 'dashboard',
		'penyisipan': penyisipan,
		'penyisipan_td': penyisipan_td,
		'pengekstrakan': pengekstrakan,
		'pengekstrakan_td': pengekstrakan_td,

	}
	return render(request, 'main/dashboard.html', context)

def Penyisipan(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = FormPenyisipan(request.POST, request.FILES)

		if form.is_valid():
			host_img = request.FILES['host_img']
			wm_img = request.FILES['wm_img']

			if ValidateImage(host_img) and ValidateImage(wm_img):
				embed_id = SlugMaker()
				image_array = cv2.imdecode(np.frombuffer(host_img.read(), np.uint8), cv2.IMREAD_COLOR)
				water_array = cv2.imdecode(np.frombuffer(wm_img.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

				result = DCT_Watermark().embed(image_array, water_array)

				img = Image.fromarray(result)
				processed_image_np = np.array(img, dtype=np.uint8)
				psnr, mse = ParameterQuality(image_array, img)

				buffer = BytesIO()
				# if GetExtension(host_img.name) == 'JPG':
				# 	img.save(buffer, format='JPEG')
				# elif GetExtension(host_img.name) == 'PNG':
				img.save(buffer, format='JPEG')
				

				data = form.save(commit=False)
				data.username = request.user.username
				data.host_img = host_img 
				data.wm_img = wm_img 
				data.psnr = psnr
				data.mse = mse
				data.embed_id = embed_id
				data.save()

				data.nama_img = Path(data.host_img.name).name
				processed_image_path = os.path.join(settings.MEDIA_ROOT, 'result', f'{host_img.name}')
				cv2.imwrite(processed_image_path, processed_image_np)
				data.result = processed_image_path
				data.save()
				buffer.close()

				messages.success(request, 'Penyisipan berhasil dilakukan!')
				context = {
					'page': 'penyisipan',
					'stage': 'output',
					'result': data.result,
					'data': embed_id,
				}
				return render(request, 'main/penyisipan.html', context)
			else:
				messages.error(request, 'Hanya gambar dengan ekstensi PNG dan JPG')
	else:
		form = FormPenyisipan()
	context = {
		'page': 'penyisipan',
		'stage': 'input',
		'form': form,
		'upimg': 'img/upload.jpg'
	}
	return render(request, 'main/penyisipan.html', context)

def Pengekstrakan(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = FormPengekstrakan(request.POST, request.FILES)

		if form.is_valid():
			host_img = request.FILES['host_img']

			if ValidateImage(host_img):
				extract_id = SlugMaker()
				host = cv2.imdecode(np.frombuffer(host_img.read(), np.uint8), cv2.IMREAD_COLOR)

				result = DCT_Watermark().extract(host)
				img = Image.fromarray(result)
				buffer = BytesIO()
				# if GetExtension(host_img.name) == 'JPG':
				# 	img.save(buffer, format='JPEG')
				# elif GetExtension(host_img.name) == 'PNG':
				img.save(buffer, format='PNG')

				data = form.save(commit=False)
				data.username = request.user.username
				data.host_img = host_img
				data.extract_id = extract_id
				data.save()

				data.nama_img = Path(data.host_img.name).name
				processed_image_np = np.array(img, dtype=np.uint8)
				cv2_image = cv2.cvtColor(processed_image_np, cv2.COLOR_RGB2BGR)
				processed_image_path = os.path.join(settings.MEDIA_ROOT, 'result', f'{extract_id}.jpg')
				cv2.imwrite(processed_image_path, cv2_image)
				data.result = processed_image_path
				data.save()
				buffer.close()

				messages.success(request, 'Pengekstrakan berhasil dilakukan!')
				context = {
					'page': 'pengekstrakan',
					'stage': 'output',
					'result': data.result,
					'data': extract_id,
				}
				return render(request, 'main/pengekstrakan.html', context)

			else:
				messages.error(request, 'Hanya gambar dengan ekstensi PNG dan JPG')
	else:
		form = FormPengekstrakan()
	context = {
		'page': 'pengekstrakan',
		'stage': 'input',
		'form': form,
		'upimg': 'img/upload.jpg'
	}
	return render(request, 'main/pengekstrakan.html', context)

def Aktivitas(request, aktivitas):
	if not request.user.is_authenticated:
		return redirect('login')

	table = None
	if aktivitas == 'penyisipan':
		table = TabelPenyisipan(ModelPenyisipan.objects.all())
	elif aktivitas == 'pengekstrakan':
		table = TabelPengekstrakan(ModelPengekstrakan.objects.all())

	table.paginate(page=request.GET.get("page", 1), per_page=5)
	context = {
		'page': 'aktivitas',
		'table': table,
		'aktivitas': aktivitas,
		'penyisipan': 'penyisipan',
		'pengekstrakan': 'pengekstrakan'
	}
	return render(request, 'main/aktivitas.html', context)

def DetailPenyisipan(request, embed_id):
	if not request.user.is_authenticated:
		return redirect('login')

	data = get_object_or_404(ModelPenyisipan, embed_id=embed_id)
	host = cv2.imread(data.host_img.path, cv2.IMREAD_COLOR)
	wm = cv2.imread(data.wm_img.path, cv2.IMREAD_GRAYSCALE)

	result = DCT_Watermark().embed_detail(host,wm)
	# print(result)
	context = {
		'page': 'detail',
		'data': data,
		'image': data.host_img,
		'water': data.wm_img,
		'ori': result[0],
		'yuv': result[1],
		'wat': result[2],
		'cov': result[3],
		'ww': result[4],
		'wh': result[5],
		'embed_pos': result[6],
		'itx': result[7],
		'ity': result[8],
		'v_1': result[9],
		'v_2': result[10],
		'v_3': result[11],
		'v_4': result[12],
		'result': data.result,
	}
	# print(data)
	return render(request, 'main/detail.html', context)

def Register(request):
	if request.user.is_authenticated:
		return redirect('login')

	if request.method == 'GET':
		form  = RegisterForm()
		context = {'form': form}
		return render(request, 'auth/register.html', context)
	if request.method == 'POST':
		form  = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Akun ' + user + ' telah dibuat')
			return redirect('login')

		else:
			# print('Form is not valid')
			messages.error(request, 'Error Processing Your Request')
			context = {'form': form}
			return render(request, 'auth/register.html', context)

	return render(request, 'auth/register.html', {})

def DownloadImage(request, embed_id):
	if not request.user.is_authenticated:
		return redirect('login')

	img = get_object_or_404(ModelPenyisipan, embed_id=embed_id)
	response = HttpResponse(img.result.read(), content_type='image/png')
	response['Content-Disposition'] = f'attachment; filename="{img.nama_img}"'
	return response

def DownloadHost(request, embed_id):
	if not request.user.is_authenticated:
		return redirect('login')

	img = get_object_or_404(ModelPenyisipan, embed_id=embed_id)
	response = HttpResponse(img.host_img.read(), content_type='image/png')
	response['Content-Disposition'] = f'attachment; filename="{img.nama_img}"'
	return response

def DownloadWatermark(request, embed_id):
	if not request.user.is_authenticated:
		return redirect('login')

	img = get_object_or_404(ModelPenyisipan, embed_id=embed_id)
	response = HttpResponse(img.wm_img.read(), content_type='image/png')
	response['Content-Disposition'] = f'attachment; filename="{img.nama_img}"'
	return response

def DownloadExtractWatermark(request, extract_id):
	if not request.user.is_authenticated:
		return redirect('login')

	img = get_object_or_404(ModelPengekstrakan, extract_id=extract_id)
	response = HttpResponse(img.result.read(), content_type='image/png')
	response['Content-Disposition'] = f'attachment; filename="{img.nama_img}"'
	return response