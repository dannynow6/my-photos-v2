#### Add Photo View Original - working on update 


# Require users to have an account before uploading a photo
@login_required
def add_photo(request):
    """a page for adding a new photo and a modal to add a new lens option"""

    if request.method == "POST":
        request.session['form_data'] = request.POST.dict() 
        # Handle the add photo form
        if "add_photo_submit" in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)

            if photo_form.is_valid():
                new_photo = photo_form.save(commit=False)
                new_photo.owner = request.user
                # Get the uploaded image from the form
                uploaded_img = new_photo.image
                new_photo.image = process_photo(uploaded_img)
                new_photo.save()
                # create a success msg to notify user
                messages.success(request, "Your photo was saved successfully!")
                # redirect user to photos page
                return redirect("photo_site:photos")

            else:
                messages.error(
                    request,
                    "There was an error in the form submission. Please check your inputs.",
                )
                return redirect("photo_site:photos")
        # Handle the add lens form
        elif "add_lens_submit" in request.POST:
            lens_form = LensForm(request.POST)
            if lens_form.is_valid():
                try:
                    lens_form.save()
                    return redirect("photo_site:add_photo")
                except IntegrityError:
                    lens_form.add_error("name", "This name already exists.")
    else:
        form_data = request.session.get('form_data', None) 
        if form_data:
            photo_form = PhotoForm(initial=form_data) 
            lens_form = LensForm()
            del request.session['form_data']
        else:
            photo_form = PhotoForm()
            lens_form = LensForm()

    context = {"photo_form": photo_form, "lens_form": lens_form}
    return render(request, "photo_site/add_photo.html", context)

