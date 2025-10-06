package com.tdebackend.clinicatde.service;

import com.tdebackend.clinicatde.model.Usuario;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AuthService {
    private final UsuarioService usuarioService;


    public AuthService(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    public String authenticate(String nome, String senha) {
        Optional<Usuario> auth = usuarioService.findByNome(nome)
                .filter(u -> u.getSenha().equals(senha));

        if (auth.isPresent()) {
            return auth.get().getTipo().toString();
        }
        return null;
    }

}
