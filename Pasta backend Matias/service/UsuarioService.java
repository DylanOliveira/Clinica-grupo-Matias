package com.tdebackend.clinicatde.service;

import com.tdebackend.clinicatde.model.Usuario;
import com.tdebackend.clinicatde.repository.UsuarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UsuarioService {
    private final UsuarioRepository repository;


    public UsuarioService(UsuarioRepository usuarioRepository) {
        this.repository = usuarioRepository;
    }

    // Create / Update
    public Usuario save(Usuario usuario) {
        return repository.save(usuario);
    }


    // Read
    public List<Usuario> findAll() {
        return repository.findAll();
    }
    public Optional<Usuario> findById(Long id) {
        return repository.findById(id);
    }
    public Optional<Usuario> findByEmail(String email) { return repository.findByEmail(email); }
    public Optional<Usuario> findByNome(String nome) { return repository.findByNome(nome); }

    // Delete
    public void deleteById(Long id) {
        repository.deleteById(id);
    }

}
