import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

enum MediaSource { video, image }

class NovoPacPage extends StatefulWidget {
  const NovoPacPage({super.key});

  @override
  State<NovoPacPage> createState({key}) => _NovoPacPageState();
}

class _NovoPacPageState extends State<NovoPacPage> {
  File? arqImagemOlho;
  File? arqImagemGuia;
  File? arqVideo;
  TextEditingController skincolorTEC = TextEditingController();

  bool loading = false;
  double progress = 0;

  downloadPhoto(File imgOlho, File imgGuia, File video, String skinColor,
      String sex) async {
    setState(() {
      loading = true;
      progress = 0;
    });

    bool downloaded = await saveMedia(imgOlho, "ft_olho.jpeg", imgGuia,
        "ft_guia.jpeg", video, "video_dedo.mp4", skinColor[0], sex[0]);
    if (downloaded) {
      // print("File Downloaded");
    } else {
      // print("Problem Downloading File");
    }
    setState(() {
      loading = false;
    });
  }

  Future<bool> saveMedia(
      File imgOlho,
      String imgOlhoName,
      File imgGuia,
      String imgGuiaName,
      File video,
      String vidName,
      String skinColor,
      String sex) async {
    Directory directory;
    try {
      if (Platform.isAndroid) {
        if (await _requestPermission(Permission.storage)) {
          directory = (await getExternalStorageDirectory())!;
          String newPath = "";
          List<String> paths = directory.path.split("/");
          for (int x = 1; x < paths.length; x++) {
            String folder = paths[x];
            if (folder != "Android") {
              newPath += "/$folder";
            } else {
              break;
            }
          }
          newPath = "$newPath/Download/mHealth_ic_app";
          directory = Directory(newPath);
        } else {
          return false;
        }
      } else {
        if (await _requestPermission(Permission.photos)) {
          directory = await getTemporaryDirectory();
        } else {
          return false;
        }
      }

      final data = DateTime.now();
      String dataStr = "$data";
      dataStr = dataStr.replaceAll(RegExp('[^A-Za-z0-9]'), '_');
      dataStr =
          '$skinColor$sex-${dataStr.substring(0, 10)}-${dataStr.substring(11, 19)}';

      File saveFileImg = File("${directory.path}/$dataStr/$imgOlhoName");
      File saveFileVid = File("${directory.path}/$dataStr/$vidName");

      if (!await directory.exists()) {
        await directory.create(recursive: true);
      }

      if (await directory.exists()) {
        String newPath = directory.path;
        newPath = "$newPath/$dataStr";
        directory = Directory(newPath);

        if (!await directory.exists()) {
          await directory.create(recursive: true);
        }

        if (await directory.exists()) {
          salvarImagem(imgOlho, directory.path, imgOlhoName);
          salvarImagem(imgGuia, directory.path, imgGuiaName);
          salvarVideo(video, directory.path, vidName);
        }

        if (Platform.isIOS) {
          await ImageGallerySaver.saveFile(saveFileImg.path,
              isReturnPathOfIOS: true);
          await ImageGallerySaver.saveFile(saveFileVid.path,
              isReturnPathOfIOS: true);
        }
        return true;
      }

      return false;
    } catch (e) {
      return false;
    }
  }

  salvarImagem(File img, String path, String fileName) async {
    // ignore: unused_local_variable
    final File localImage = await img.copy('$path/$fileName');
  }

  salvarVideo(File video, String path, String fileName) async {
    // ignore: unused_local_variable
    final File localImage = await video.copy('$path/$fileName');
  }

  Future<bool> _requestPermission(Permission permission) async {
    if (await permission.isGranted) {
      return true;
    } else {
      var result = await permission.request();
      if (result == PermissionStatus.granted) {
        return true;
      }
    }
    return false;
  }

  // Possíveis cores de pele e sexo
  List<String> coresPele = ["--------", "Negro", "Pardo", "Branco"];
  String corPeleSelecionada = "--------";
  List<String> sexo = ["--------", "Masculino", "Feminino"];
  String sexoSelecionado = "--------";

  // Construção da tela
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 84.0),
      child: Scaffold(
        body: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 80.0),
              child: SizedBox(
                width: 165,
                child: DropdownButtonFormField<String>(
                    decoration: const InputDecoration(border: InputBorder.none),
                    value: corPeleSelecionada,
                    items: coresPele
                        .map((item) => DropdownMenuItem<String>(
                            value: item,
                            child: Text(
                              item,
                              style: const TextStyle(
                                  color: Color.fromARGB(155, 0, 0, 0)),
                            )))
                        .toList(),
                    onChanged: (item) =>
                        setState(() => corPeleSelecionada = item!)),
              ),
            ),
            SizedBox(
              width: 165,
              child: DropdownButtonFormField<String>(
                  decoration: const InputDecoration(border: InputBorder.none),
                  value: sexoSelecionado,
                  items: sexo
                      .map((item) => DropdownMenuItem<String>(
                          value: item,
                          child: Text(
                            item,
                            style: const TextStyle(
                                color: Color.fromARGB(155, 0, 0, 0)),
                          )))
                      .toList(),
                  onChanged: (item) => setState(() => sexoSelecionado = item!)),
            ),
            ListTile(
              leading: const Icon(
                Icons.remove_red_eye,
                color: Colors.grey,
              ),
              title: const Text(
                'Foto do olho',
                style: TextStyle(color: Color.fromARGB(155, 0, 0, 0)),
              ),
              onTap: () => capture(MediaSource.image, 0),
            ),
            ListTile(
              leading: const Icon(
                Icons.article,
                color: Colors.grey,
              ),
              title: const Text(
                'Foto da guia',
                style: TextStyle(color: Color.fromARGB(155, 0, 0, 0)),
              ),
              onTap: () => capture(MediaSource.image, 1),
            ),
            ListTile(
              leading: const Icon(
                Icons.camera_alt,
                color: Colors.grey,
              ),
              title: const Text(
                'Vídeo do dedo',
                style: TextStyle(color: Color.fromARGB(155, 0, 0, 0)),
              ),
              onTap: () => capture(MediaSource.video, -1),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 35.0),
              child: ElevatedButton(
                onPressed: () => {
                  if (arqImagemOlho != null &&
                      arqImagemGuia != null &&
                      arqVideo != null)
                    downloadPhoto(arqImagemOlho!, arqImagemGuia!,
                        arqVideo!, corPeleSelecionada, sexoSelecionado),
                  corPeleSelecionada = "--------",
                  sexoSelecionado = "--------",
                  arqImagemOlho = null,
                  arqImagemGuia = null,
                  arqVideo = null,
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green.shade300,
                ),
                child: const Text(
                  'Salvar',
                  style: TextStyle(color: Colors.black),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future capture(MediaSource source, int selectFlag) async {
    final PickedFile? media;
    source == MediaSource.image
        ? media = await ImagePicker().getImage(source: ImageSource.camera)
        : media = await ImagePicker().getVideo(
            source: ImageSource.camera,
            maxDuration: const Duration(seconds: 36),
          );

    if (source == MediaSource.video) {
      arqVideo = File(media!.path);
    } else if (selectFlag == 0) {
      // Foto do olho.
      arqImagemOlho = File(media!.path);
    } else {
      // Foto da guia.
      arqImagemGuia = File(media!.path);
    }
  }
}
