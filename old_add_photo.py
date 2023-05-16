
    if request.method != "POST":
        form = PhotoForm()
    else:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.owner = request.user
            new_photo.save()
            return redirect("photo_site:index")

    context = {"form": form}
    return render(request, "photo_site/add_photo.html", context)




@login_required
def lens(request):
    """add a new lens to the list of lenses"""
    if request.method != "POST":
        # blank form
        form = LensForm()
    else:
        # POST data submitted and process
        form = LensForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("photo_site:add_photo")
    context = {"form": form}
    return render(request, "photo_site/lens.html", context)

lens = models.CharField(max_length=200, blank=True, null=True)