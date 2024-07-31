import 'package:flutter/material.dart';
import 'package:primeiro_app/pac_cad.dart';

import 'novo_pac.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int pagEscolhida = 0;

  void _onItemTapped(int index) {
    setState(() {
      pagEscolhida = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: pagEscolhida,
        // ignore: prefer_const_literals_to_create_immutables
        children: <Widget>[
          // ignore: prefer_const_constructors
          PacCadPage(),
          const NovoPacPage(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.archive_outlined),
            label: 'Pacientes Cadastrados',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.add),
            label: 'Novo Paciente',
          ),
        ],
        backgroundColor: Colors.red.shade200,
        currentIndex: pagEscolhida,
        selectedItemColor: Colors.black,
        onTap: _onItemTapped,
      ),
    );
  }
}
